use std::io;

fn main() {

    println!("Ingrese un número entero n:");

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Error al leer");

    let n: i32 = match input.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Entrada inválida");
            return;
        }
    };

    if n < 0 {
        println!("El número debe ser mayor o igual a 0");
        return;
    }

    let mut enteros = Vec::new();
    let mut pares = Vec::new();
    let mut impares = Vec::new();
    let mut primos = Vec::new();

    for i in 0..=n {

        enteros.push(i);

        if i % 2 == 0 {
            pares.push(i);
        } else {
            impares.push(i);
        }

        if i >= 2 {
            let mut primo = true;

            for j in 2..=((i as f64).sqrt() as i32) {
                if i % j == 0 {
                    primo = false;
                    break;
                }
            }

            if primo {
                primos.push(i);
            }
        }
    }

    println!("Enteros: {:?}", enteros);
    println!("Pares: {:?}", pares);
    println!("Impares: {:?}", impares);
    println!("Primos: {:?}", primos);
}

