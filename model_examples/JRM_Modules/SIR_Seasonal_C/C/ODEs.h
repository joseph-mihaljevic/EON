// --------------------------------Begin ODE system of White model --------------------------------------------//
int fast_odes(double t, const double y[], double dydt[],void *Paramstuff)
{
  //struct STRUCTURE *Params=(struct STRUCTURE *)Paramstuff;
  ParamStruct* ODEParams;
  ODEParams = (ParamStruct*) Paramstuff;
  
  double beta0 = ODEParams->beta0;
  double beta1 = ODEParams->beta1;
  double gam = ODEParams->gam;
  double mu = ODEParams->mu;

  // ------------------------------------------ ODEs -------------------------------------------- //
  
  double beta_forced = beta0 * (1 + beta1 * sin(2*pi*t/365) );
  
  dydt[0] = mu - beta_forced*y[0]*y[1] - mu*y[0]; //dS
  dydt[1] = beta_forced*y[0]*y[1] - (mu + gam)*y[1]; //dI
  
  return GSL_SUCCESS;
}


// ------------------------------------------  ODE Solver  ----------------------------------------------- //
double ODE_Solver(double t_ode,double t_end, void *Paramstuff,double *y_ode)
{
    int i;
    int status_ode;
    double h_init=1.0e-5;
    
    ParamStruct* ODEParams;
    ODEParams = (ParamStruct*) Paramstuff;
    
    // Total number of ODEs
    int DIM = 2; 
    
    const gsl_odeiv2_step_type *solver_ode	= gsl_odeiv2_step_rkf45; // Runge-Kutta Fehlberg (4, 5)

    gsl_odeiv2_step *step_ode	= gsl_odeiv2_step_alloc(solver_ode, DIM);
    
    gsl_odeiv2_control *tol_ode	= gsl_odeiv2_control_standard_new(1.0e-10, 1.0e-5, 1.0, 0.2);
    
    gsl_odeiv2_evolve *evol_ode	= gsl_odeiv2_evolve_alloc(DIM);
    
    //gsl_odeiv_system sys_ode;
    gsl_odeiv2_system sys_ode;
    sys_ode.function  = fast_odes;
    sys_ode.jacobian  = NULL;
    sys_ode.dimension = (size_t)(DIM);
    sys_ode.params	  = ODEParams;
    
    //double y_err[DIM]; double dydt_in[DIM];	double dydt_out[DIM];
    
    // ----------------------------------- Integrate Over Time ------------------------------------ //
    
    
    
    while (t_ode<t_end)	{
        
        
        status_ode = gsl_odeiv2_evolve_apply(evol_ode, tol_ode, step_ode, &sys_ode, &t_ode, t_end, &h_init, y_ode);
        
        //status_ode = gsl_odeiv2_step_apply(step_ode, t_ode, h_init, y_ode, y_err, dydt_in, dydt_out, &sys_ode);
        
        
        
        for (i=0;i<DIM;i++)	{
            
            if(y_ode[i]<0) y_ode[i] = 0.0;
            
        }

    }
    // -------------------------------------- Clear Memory ----------------------------------------- //
    
    
    gsl_odeiv2_evolve_free(evol_ode);
    gsl_odeiv2_control_free(tol_ode);
    gsl_odeiv2_step_free(step_ode);
    
    return (t_end);
}


