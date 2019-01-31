float RK45_Integrate(ParamStruct Params, gsl_rng *rand1, int iter){
  
  //*****************************************
  // Output:
  FILE *fp;
  if(Figures) 
    fp = fopen("./output/Stoch_SIR_Hetero.dat","a");
  
  ParamStruct ODEParams;
  ODEParams = Params;
  
  int n_day;
  n_day = ODEParams.n_day;
  
  double time_step;
  time_step = ODEParams.time_step;
  
  double N0, Y0, X0;
  N0 = ODEParams.N0; 
  Y0 = ODEParams.Y0; 
  X0 = ODEParams.X0;
  
  double t;
  
  // For stochasticity
  double rand_draw, noise, hetero_A;
  hetero_A = ODEParams.hetero_A;
  double beta_adj, beta_bar, beta_var;
  beta_bar = ODEParams.beta_bar;
  beta_var = ODEParams.beta_var;

  //Store Output:
  float OUT;
  
  //*****************************************
  
  // Set up initial conditions
  double y_ode[2]; //dS, dI
  
  y_ode[0] = X0;
  y_ode[1] = Y0; 
  
  //*****************************************
  
  // Start the ODE routine:
  
  //Loop over t
  t = 0;

  while((t < n_day)){
    
    
    if(Figures){
      //Print: Day, S, I
      //printf(fp, "%d %f %f %f\n", iter, t, y_ode[0], y_ode[1]);
      fprintf(fp, "%d %f %f %f\n", iter, t, y_ode[0], y_ode[1]);
    }
    
    ///////////////////  Here is the ODE solver at work ///////////////////
    double t_next = t + time_step;
    
    // Stochastic Noise:
    noise = gsl_ran_ugaussian(rand1) * beta_var / sqrt(time_step);
    ODEParams.noise = noise;
    
    //printf("Up to ODE_Solver.\n");
    t = ODE_Solver(t, t_next, &ODEParams, y_ode); //Numerical integration from t to t_next, returns (t_end)
    //printf("After ODE_Solver.\n");
    

  } // t loop 
  
  
  if(Figures==1){ 
    fclose(fp);
  }
  
  
  OUT = 0.0;
  
  return OUT;
  
}  //The End






