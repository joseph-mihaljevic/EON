float RK45_Integrate(ParamStruct Params){

  //*****************************************
  // Output:
  FILE *fp;
  if(Figures)
    fp = fopen("./output.csv","a");

  ParamStruct ODEParams;
  ODEParams = Params;

  int n_day;
  n_day = ODEParams.n_day;

  double S0, I0;
  S0 = ODEParams.S0; //printf("S0 = %f\n", S0);
  I0 = ODEParams.I0; //printf("I0 = %f\n", I0);

  double t;

  //Store Output:
  float OUT;

  //*****************************************

  // Set up initial conditions
  double y_ode[2]; //dS, dI

  y_ode[0] = S0;
  y_ode[1] = I0;

  //*****************************************

  // Start the ODE routine:

  //Loop over t
  t = 0;

  if(Figures){
    //Print: Column names
    fprintf(fp, "Year, Day, S, I\n");
  }

  while((t < n_day)){


    if(Figures){
      //Print: Year, Day, S, I
      fprintf(fp, "%f,%f,%f,%f", (t/365 + 1), t, y_ode[0], y_ode[1]);
      if(t < (n_day-1)){
        fprintf(fp, "\n");
      }
    }

    ///////////////////  Here is the ODE solver at work ///////////////////
    double t_next = t + 1;

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
