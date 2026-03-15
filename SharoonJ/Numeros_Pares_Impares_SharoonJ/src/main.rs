use std::io;

fn main() {
    let mut entrada = String::new();

    println!("Ingrese un numero entero positivo:");

    io::stdin()
        .read_line(&mut entrada)
        .expect("0_0 Error al leer");

    let n: i32 = match entrada.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Error >_< debe ingresar un numero entero.");
            return;
        }
    };

    if n <= 0 {
        println!("Error *_* ingrece un numero entero positivo.");
        return;
    }

    let mut pares = Vec::new();
    let mut impares = Vec::new();
    let mut primos = Vec::new();
    let mut lista = Vec::new();

    for i in 1..=n {
        lista.push(i);

        if i % 2 == 0 {
            pares.push(i);
        } else {
            impares.push(i);
        }
    }

    // Numeros primos
    for i in 2..=n {
        let mut es_primo = true;

        for j in 2..i {
            if i % j == 0 {
                es_primo = false;
                break;
            }
        }

        if es_primo {
            primos.push(i);
        }
    }

    println!("Lista de numeros: {:?}", lista);
    println!("Lista de primos: {:?}", primos);
    println!("Pares: {:?}", pares);
    println!("Impares: {:?}", impares);

    println!("Cantidad de pares: {}", pares.len());
    println!("Cantidad de impares: {}", impares.len());
}