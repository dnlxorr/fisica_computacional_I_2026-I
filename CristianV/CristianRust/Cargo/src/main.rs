mod variable;
mod pares_impares;
mod tiempo_ejecucion;
mod clima_grafica1;
mod taylo_aprox;
mod stack_queue;
mod Error_Conteo;

fn main() {
    // print!("Ejecucion de tiempo \n");
    // tiempo_ejecucion::tiempo_eje();
    // print!("Ejecucion de variable\n ");
    // variable::aja();
    // print!("Ejecucion de Primos, Pares e Impares\n");
    // pares_impares::num_pares_impares_primos();
    // print!("Ejecucion de grafica 1\n");
    // clima_grafica1::clima().expect("REASON")
    // print!("Funcion de aproximacion por taylo");
    // taylo_aprox::aprox();
    // print!("Funcion de aproximacion por taylo");
    // stack_queue::st_qu();
    print!("Error de redondeo");
    Error_Conteo::errorcon();
}