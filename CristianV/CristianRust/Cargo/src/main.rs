mod variable;
mod pares_impares;
mod tiempo_ejecucion;



fn main() {
    print!("Ejecucion de tiempo \n");
    tiempo_ejecucion::tiempo_eje();
    print!("Ejecucion de variable\n ");
    variable::aja();
    print!("Ejecucion de Primos, Pares e Impares\n");
    pares_impares::num_pares_impares_primos();
}