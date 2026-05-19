use std::io;

pub(crate) fn numeros() {

    let mut entrada = String::new();

    println!("Ingrese el número máximo :  ");
    io::stdin()
        .read_line(&mut entrada)
        .expect("Error al leer la entrada");

    let entrada: usize = entrada.trim().parse().expect("Por favor ingrese un número");

    let mut lista: Vec<usize> = (0..=entrada).collect();
    let mut pares: Vec<usize> = Vec::new();
    let mut impares: Vec<usize> = Vec::new();

    let mut primos: Vec<bool> = vec![true; entrada + 1];
    primos[0] = false;
    primos[1] = false;

    let mut lista_primos: Vec<usize> = Vec::new();

    for n in 0..=entrada {
        if n % 2 == 0 {
            pares.push(n);
        } else {
            impares.push(n);
        }
    }

    for i in 2..=entrada {
        if primos[i] == true {
            let mut j = i * 2;
            while j <= entrada {
                primos[j] = false;
                j += i;
            }
        }
    }

    for i in 2..=entrada {
        if primos[i] == true {
            lista_primos.push(i);
        }
    }

    println!("La lista de números es: {:?} ", lista);
    println!("los numero pares son:  {:?}", pares);
    println!("La cantidad de números pares es: {}", pares.len());
    println!("los numero impares son:  {:?}", impares);
    println!("La cantidad de números impares es: {}", impares.len());
    println!("Los números primos encontrados son: {:?}", lista_primos);
    println!("La cantidad de números primos es: {}", lista_primos.len());

}