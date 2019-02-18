'''data_processing.py - Joshua Wallace - Feb 2019

This code is where the rubber meets the road: where the light curve
data actually gets fed in and results actually get calculated.
'''

from light_curve_class import lc_objects
import simple_deblend
from multiprocessing import Pool, cpu_count
from astrobase.periodbase.zgls import pgen_lsp as ls_p
from astrobase.periodbase.spdm import stellingwerf_pdm as pdm_p
from astrobase.periodbase.kbls import bls_parallel_pfind as bls_p





class lc_collection_for_processing(lc_objects):
    '''This is the "master class", as it were, of this package.  The methods
    of this class are what actually lead to periods being found, checked,
    calculated, removed, etc. and it is the main way to access the
    abilities of the code

    Subclasses light_curve_class.lc_objects

    The initialization takes one argument and one optional argument:
    radius   - the circular radius, in pixels, for objects to be in 
               sufficient proximity to be regarded as neighbors
    nworkers - (optional; default None) the number of workers to use in the
               parallel calculation---value of None defaults to 
               multiprocessing.cpu_count
    '''
    def __init__(self,radius_,nworkers=None):
        lc_objects.__init__(self,radius_)
        if not nworkers:
            self.nworkers = cpu_count
        elif nworkers > cpu_count():
            print("nworkers was greater than number of CPUs, setting instead to " + str(cpu_count))
            self.nworkers = cpu_count
        else:
            self.nworkers = nworkers
        #self._acceptable_methods = ['LS','BLS','PDM']
        self.results = {}


    def run_ls(self,startp=None,endp=None,autofreq=True,
                   nbestpeaks=3,periodepsilon=0.1,stepsize=1.0e-4,
                   sigclip=float('inf')):

        params = {startp:startp,endp:endp,autofreq:autofreq,
                      nbestpeaks:nbestpeaks,periodepsilon:periodepsilon,
                      stepsize:stepsize,sigclip:sigclip}

        self.run('LS',ls_p,params)

        
    def run_pdm(self,startp=None,endp=None,autofreq=True,
                     nbestpeaks=3,periodepsilon=0.1,stepsize=1.0e-4,
                     sigclip=float('inf')):

        params = {startp:startp,endp:endp,autofreq:autofreq,
                      nbestpeaks:nbestpeaks,periodepsilon:periodepsilon,
                      stepsize:stepsize,sigclip:sigclip}

        self.run('PDM',pdm_p,params)

    def run_bls(self,startp=None,endp=None,autofreq=True,
                     nbestpeaks=3,periodepsilon=0.1,stepsize=1.0e-4,
                     sigclip=float('inf')):

        params = {startp:startp,endp:endp,autofreq:autofreq,
                      nbestpeaks:nbestpeaks,periodepsilon:periodepsilon,
                      stepsize:stepsize,sigclip:sigclip}

        self.run('BLS',bls_p,params)
        

    def run(self,which_method,ps_func,params):

        mp_pool = Pool(self.nworkers)

        _ = pool.starmap(self._run_single_object, [(o,which_method,ps_func,
                                                        params)
                                                       for o in self.objects])

    def _run_single_object(self,object,which_method,ps_func):

        # Actually, just try John's function
        neighbor_lightcurves = [(self.lc_objects.objects[self.lc_objects.objects.index_dict[neighbor_ID]].times,
                                     self.lc_objects.objects[self.lc_objects.objects.index_dict[neighbor_ID]].mags,
                                     self.lc_objects.objects[self.lc_objects.objects.index_dict[neighbor_ID]].errs) for neighbor_ID in object.neighbors]


        results_storage = periodsearch_results(object.ID)

        for _ in range(parms['nbestpeaks']):
            rv = iterative_deblend(object.times,object.mags,object.errs,
                                    neighbor_lightcurves,pgen,
                                    results_storage,
                                    function_parms=parms,
                                    nharmonics_fit=7,
                                    max_fap=.5)
            if rv is None:
                    break

        if len(results_storage.good_periods_info) > 0:
            self.results[object.ID][method] = rv
        #else:
        #    all_results[method] = None

        #if not all
        #with open(output_dir + "periodsearch_" + object.ID + ".pkl") as f:
        #    pickle.dump(results_storage,f)

        ###### So what kind of information do I want returned?
          # LSP of any well-found peak
          # Record of which periods (and epochs) were blends
          # Fourier-fitted lc's


    def save_periodsearch_results(self,outputdir):
        for o in self.objects:
            if o.ID in self.results.keys():
                with open(outputdir + "ps_" + o.ID + ".pkl","wb") as f:
                    pickle.dump(self.results[o.ID],f)
        

            

class periodsearch_results():
    def __init__(self,ID_):
        self.ID = ID_
        self.good_periods_info = []
        self.blends_info = []

    def add_good_period(self,lsp_dict,times,mags,errs,fap):
        dict_to_add = {'lsp_dict':lsp_dict,'times':times,
                           'mags':mags,'errs':errs,'fap':fap,
                           'num_previous_blends':len(self.blends_info)}
        self.good_periods_info.append(dict_to_add)

    def add_blend(self,lsp_dict,neighbor_ID,fap):
        dict_to_add = {'lsp_dict':lsp_dict,
                           'ID_of_blend':neighbor_ID,
                           'fap':fap,
                           'num_previous_signals':len(self.good_periods_info)}
        self.blend_info.append(dict_to_add)


