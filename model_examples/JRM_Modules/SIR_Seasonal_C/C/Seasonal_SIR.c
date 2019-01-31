//Parameter structure type:
typedef struct {
  // param: nyear = 50
  double beta0; // 1.5
  double beta1; // default: .25 changeable: corresponds to strength of forcing 0-.75
  double gam; // 1/13=0.07692307692
  double mu; // 1/(50*365)=0.00005479452
  double S0; // .75
  double I0; // .25
  //ODE control:
  int n_day;

} ParamStruct;


int Figures = 1;
#define pi 3.1415927

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
  int n_year, n_day;
  n_year = atoi(argv[1]);
  n_day = 365 * n_year;

  // Allocate variables / parameters:
  ParamStruct Params;

  double beta0, beta1, gam, mu, S0, I0;
  beta0 = atof(argv[2]);
  beta1 = atof(argv[3]);
  gam = atof(argv[4]);
  mu = atof(argv[5]);
  S0 = atof(argv[6]);
  I0 = atof(argv[7]);


  Params.beta0 = beta0;
  Params.beta1 = beta1;
  Params.gam = gam;
  Params.mu = mu;
  Params.S0 = S0;
  Params.I0 = I0;
  Params.n_day = n_day;

  float ode_out;

  ode_out = RK45_Integrate(Params);

  return 0;

}
