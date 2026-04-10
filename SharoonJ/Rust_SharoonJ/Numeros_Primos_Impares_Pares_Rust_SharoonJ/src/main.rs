use std::io;

fn main() {

    println!("Ingrese un numero entero positivo:");

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Error al leer");

    let n: i32 = match input.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Error 0_o Debe ingresar un numero entero positivo");
            return;
        }
    };

    if n <= 0 {
        println!("Error >_< ingresar un numero entero positivo.");
    } else {

        let mut pares: Vec<i32> = Vec::new();
        let mut impares: Vec<i32> = Vec::new();
        let mut primos: Vec<i32> = Vec::new();

        let lista: Vec<i32> = (1..=n).collect();

        for i in 1..=n {

            // Pares e impares
            if i % 2 == 0 {
                pares.push(i);
            } else {
                impares.push(i);
            }
        }

        // Primos
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

        // Impresión
        println!("Lista de numeros: {:?}", lista);
        println!("Lista de primos: {:?}", primos);

        println!("Numeros Pares: {:?}", pares);
        println!("Numeros Impares: {:?}", impares);

        println!("Cantidad de Pares: {}", pares.len());
        println!("Cantidad de Impares: {}", impares.len());
    }
}