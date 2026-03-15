use std::io::{self, Write};

pub(crate) fn num_pares_impares_primos() {
    // 1. Lectura de datos
    print!("Ingresa los números separados por espacios: ");
    io::stdout().flush().unwrap(); // Asegura que el mensaje se imprima antes del input

    let mut entrada = String::new();
    io::stdin().read_line(&mut entrada).expect("Error al leer");

    let mut numeros: Vec<i32> = Vec::new();

    // 2. Procesamiento de la entrada
    for valor in entrada.split_whitespace() {
        match valor.parse::<i32>() {
            Ok(n) => numeros.push(n),
            Err(_) => println!("Ingreso un caracter incompatible: {}", valor),
        }
    }

    let mut pares = Vec::new();
    let mut impares = Vec::new();
    let mut primos = Vec::new();

    // 3. Clasificación de pares e impares
    for &n in &numeros {
        if n % 2 == 0 {
            pares.push(n);
        } else {
            impares.push(n);
        }
    }

    // 4. Identificación de números primos
    for &m in &numeros {
        if m > 1 {
            let mut es_primo = true;
            let limite = (m as f64).sqrt() as i32;

            for i in 2..=limite {
                if m % i == 0 {
                    es_primo = false;
                    break;
                }
            }

            if es_primo {
                primos.push(m);
            }
        }
    }

    // 5. Salida de resultados
    println!("La lista de números es: {:?}", numeros);
    println!("La lista de pares son: {:?}", pares);
    println!("Los números pares son: {}", pares.len());
    println!("La lista de impares son: {:?}", impares);
    println!("Los números de impares es: {}", impares.len());
    println!("La lista de primos son: {:?}", primos);
    println!("Los números primos son: {}", primos.len());
}