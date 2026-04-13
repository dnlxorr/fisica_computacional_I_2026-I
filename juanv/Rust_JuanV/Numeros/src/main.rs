use std::io;

fn es_primo(num: u32) -> bool {
    if num < 2 {
        return false;
    }
    for i in 2..=((num as f64).sqrt() as u32) {
        if num % i == 0 {
            return false;
        }
    }
    true
}

fn main() {
    println!("Ingrese un número entero positivo:");

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Error al leer la entrada");

    match input.trim().parse::<u32>() {
        Ok(n) => {
            if n <= 0 {
                println!("Error >_< ingresar un número entero positivo.");
            } else {
                // Lista principal
                let lista: Vec<u32> = (1..=n).collect();

                // Pares e impares
                let pares: Vec<u32> = lista.iter().cloned().filter(|x| x % 2 == 0).collect();
                let impares: Vec<u32> = lista.iter().cloned().filter(|x| x % 2 != 0).collect();

                // Primos
                let primos: Vec<u32> = lista.iter().cloned().filter(|x| es_primo(*x)).collect();

                // Impresión
                println!("Lista de números: {:?}", lista);
                println!("Lista de primos: {:?}", primos);

                println!("Números Pares: {:?}", pares);
                println!("Números Impares: {:?}", impares);

                println!("Cantidad de Pares: {}", pares.len());
                println!("Cantidad de Impares: {}", impares.len());
            }
        }
        Err(_) => {
            println!("Error 0_o Debe ingresar un número entero positivo");
        }
    }
}
