pub(crate)fn variables() {
    // =========================================
    // TIPOS DE VARIABLES
    // =========================================

    let entero: i32 = 10;
    let flotante: f64 = 2.5;
    let texto: &str = "Hola";
    let booleano: bool = true;

    println!("Variables:");
    println!("{}", entero);
    println!("{}", flotante);
    println!("{}", texto);
    println!("{}", booleano);

    // =========================================
    // ESTRUCTURAS DE CONTROL
    // =========================================

    let x = 7;

    if x > 10 {
        println!("Mayor que 10");
    } else if x == 10 {
        println!("Igual a 10");
    } else {
        println!("Menor que 10");
    }

    // for (rango)
    println!("\nFor:");
    for i in 0..3 {
        println!("{}", i);
    }

    // while
    println!("\nWhile:");
    let mut contador = 0;

    while contador < 3 {
        println!("{}", contador);
        contador += 1;
    }
}