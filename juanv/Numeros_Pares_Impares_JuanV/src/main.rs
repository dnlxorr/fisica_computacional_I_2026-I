use std::io;

fn es_primo(numero: i32) -> bool {
    if numero < 2 {
        return false;
    }

    for i in 2..=((numero as f64).sqrt() as i32) {
        if numero % i == 0 {
            return false;
        }
    }

    true
}

fn main() {
    let mut texto = String::new();

    println!("Digite un numero entero positivo:");

    io::stdin()
        .read_line(&mut texto)
        .expect("Error al capturar el numero");

    let numero: i32 = match texto.trim().parse() {
        Ok(valor) => valor,
        Err(_) => {
            println!("Debe ingresar un numero valido.");
            return;
        }
    };

    if numero <= 0 {
        println!("El numero debe ser positivo.");
        return;
    }

    let mut lista_numeros = Vec::new();
    let mut numeros_pares = Vec::new();
    let mut numeros_impares = Vec::new();
    let mut numeros_primos = Vec::new();

    for x in 1..=numero {
        lista_numeros.push(x);

        if x % 2 == 0 {
            numeros_pares.push(x);
        } else {
            numeros_impares.push(x);
        }

        if es_primo(x) {
            numeros_primos.push(x);
        }
    }

    println!("Numeros generados: {:?}", lista_numeros);
    println!("Numeros primos: {:?}", numeros_primos);
    println!("Pares: {:?}", numeros_pares);
    println!("Impares: {:?}", numeros_impares);

    println!("Total de pares: {}", numeros_pares.len());
    println!("Total de impares: {}", numeros_impares.len());
}