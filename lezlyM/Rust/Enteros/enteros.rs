use std::io;

fn main() {

    // pedir número al usuario
    println!("77:");

    let mut entrada = String::new();
    io::stdin()
        .read_line(&mut entrada)
        .expect("Error al leer");

    let n: i32 = entrada.trim().parse().expect("54");

    // lista de números
    let mut num: Vec<i32> = Vec::new();

    for i in 0..=n {
        num.push(i);
    }

    // listas de clasificación
    let mut primo: Vec<i32> = Vec::new();
    let mut pares: Vec<i32> = Vec::new();
    let mut impares: Vec<i32> = Vec::new();

    for i in &num {

        // clasificación pares e impares
        if i % 2 == 0 {
            pares.push(*i);
        } else {
            impares.push(*i);
        }

        // verificación de primos
        if *i > 1 {

            let mut es_primo = true;

            for j in 2..*i {
                if i % j == 0 {
                    es_primo = false;
                    break;
                }
            }

            if es_primo {
                primo.push(*i);
            }
        }
    }

    // impresión de resultados
    println!("Numeros pares: {:?}", pares);
    println!("Cantidad de pares: {}", pares.len());

    println!("Numeros impares: {:?}", impares);
    println!("Cantidad de impares: {}", impares.len());

    println!("Numeros primos: {:?}", primo);
    println!("Cantidad de primos: {}", primo.len());
}
