#include <stdio.h>
#include <stdlib.h>

int main()
{
//------------------------------------------------
  // Medidas 
  // Verdadeiros positivos
  int vp = 1;
  // Falsos negativos
  int fn = 1;
  // Falsos positivos
  int fp = 1;
  // Verdadeiros negativos
  int vn = 1;
//------------------------------------------------
  // Cálculos
  double precisao = (vp * 1.0) / (vp + fp);
  double recall =   (vp * 1.0) / (vp + fn);
  double f1 =       2*recall*precisao / (recall + precisao);

  double tvp = (vp * 1.0) / (vp + fn);
  double tfn = (fn * 1.0) / (vp + fn);
  double tfp = (fp * 1.0) / (fp + vn);
  double tvn = (vn * 1.0) / (fp + vn);
//------------------------------------------------
  // Resultados
  printf("\n Precisao: %lf", precisao);
  printf("\n Recall: %lf", recall);
  printf("\n F1Score: %lf", f1);
  printf("\n TVP: %d/%d = %lf", vp, (vp+fn), tvp);
  printf("\n TFN: %d/%d = %lf", fn, (vp+fn), tfn);
  printf("\n TFP: %d/%d = %lf", fp, (fp+vn), tfp);
  printf("\n TVN: %d/%d = %lf", vn, (fp+vn), tvn);
  printf("\n");
//------------------------------------------------
}
