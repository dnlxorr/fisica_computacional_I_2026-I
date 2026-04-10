fn main() {

    // ===== Variables =====

    let entero: i32 = 10;          // número entero
    let decimal: f64 = 3.14;       // número decimal
    let booleano: bool = true;     // valor lógico
    let texto: &str = "Hola Rust"; // cadena de texto

    println!("Entero: {}", entero);
    println!("Decimal: {}", decimal);
    println!("Booleano: {}", booleano);
    println!("Texto: {}", texto);


    // ===== Variable mutable =====

    let mut contador = 0;
    contador = contador + 1;
    println!("Contador: {}", contador);


    // ===== Condicional if =====

    if entero > 5 {
        println!("El entero es mayor que 5");
    } else {
        println!("El entero es menor o igual que 5");
    }


    // ===== match (similar a switch) =====

    match contador {
        0 => println!("Contador es cero"),
        1 => println!("Contador es uno"),
        _ => println!("Otro valor"),
    }


    // ===== Bucle for =====

    for i in 0..5 {
        println!("For: {}", i);
    }


    // ===== Bucle while =====

    let mut i = 0;

    while i < 3 {
        println!("While: {}", i);
        i += 1;
    }


    // ===== Bucle loop =====

    let mut j = 0;

    loop {
        println!("Loop: {}", j);

        if j == 2 {
            break;
        }

        j += 1;
    }
}