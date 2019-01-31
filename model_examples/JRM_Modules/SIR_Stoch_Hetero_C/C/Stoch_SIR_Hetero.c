//Parameter structure type:
typedef struct {
  
  double beta_bar;
  double beta_var;
  double hetero_A;
  double gam;
  double mu;
  double N0;
  double Y0;
  double X0;
  double noise;
  
  //ODE control:
  int n_day;
  double time_step;
  
} ParamStruct;


int Figures = 1;

#include <time.h>
#include "stdio.h"
#include "string.h"
#include <stdlib.h>
#include <omp.h>
#include <unistd.h>
#include <uuid/uuid.h>

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
#include <gsl/gsl_sf_gamma.h>
#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>
#include <gsl/gsl_errno.h>	// GSL_SUCCEnn ...
#include <gsl/gsl_odeiv2.h>	// ODE solver

#include <gsl/gsl_types.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_min.h>

#include <gsl/gsl_math.h>

#include "math.h"
#include "stdio.h"

//Custom headers
#include "ODEs.h"

//Custom headers and functions:
#include "Nrutil.c"
#include "RK45_Integrate.c"

gsl_rng *rand1;  //This has to be global, to ensure that the generator doesn't start over again.

int main(int argc, char *argv[]){
  
  //*****************************************
  
  // Allocate random numbers structures:
  long seed;
  srand((unsigned) time(NULL));
  seed = time(NULL)*(int)getpid();
  
  int pid;
  pid = getpid();
  
  gsl_rng_env_setup ();
  gsl_rng_default_seed = seed;
  const gsl_rng_type *T1;
  T1 = gsl_rng_default;
  rand1 = gsl_rng_alloc(T1);
  
  //printf("Done with rand structure.\n");
  
  // TEST UUID
  
  // uuid_t uuid;
  // uuid_generate_random(uuid);
  // char uuid_str[37];
  // uuid_unparse_lower(uuid, uuid_str);
  // printf("uuid: %s\n", uuid_str);
  
  //*****************************************
  
  //ODE control:
  int n_year, n_day, n_iter;
  n_year = atoi(argv[1]);
  n_day = 365 * n_year;
  n_iter = atoi(argv[2]);
  
  double time_step;
  time_step = atof(argv[3]);
  
  // Allocate variables / parameters:
  ParamStruct Params;
  
  double beta_bar, beta_var, hetero_A, gam, mu, N0, Y0, X0;
  beta_bar = atof(argv[4]); 
  beta_var = atof(argv[5]); 
  hetero_A = atof(argv[6]);
  gam = atof(argv[7]); 
  mu = atof(argv[8]); 
  N0 = atof(argv[9]); 
  Y0 = atof(argv[10]); 
  X0 = atof(argv[11]);
  
  Params.beta_bar = beta_bar;
  Params.beta_var = beta_var;
  Params.hetero_A = hetero_A;
  Params.gam = gam;
  Params.mu = mu;
  Params.N0 = N0;
  Params.Y0 = Y0;
  Params.X0 = X0;
  Params.n_day = n_day;
  Params.time_step = time_step;
  
  float ode_out;
  
  int i;
  
  for(i=1;i<=n_iter;i++){
      
      ode_out = RK45_Integrate(Params, rand1, i);
    
  }
  
  
  return 0;
  
}