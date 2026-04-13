// clasificacion de numeros
fn clasificar_numeros(n: i32) {
    let mut pares = Vec::new();
    let mut impares = Vec::new();
    let mut primos = Vec::new();

    for num in 1..=n {
        // Clasificación de Pares e Impares
        if num % 2 == 0 {
            pares.push(num);
        } else {
            impares.push(num);
        }

        // Clasificación de Primos
        if num > 1 {
            let mut es_primo = true;
            let limite = (num as f64).sqrt() as i32;

            for i in 2..=limite {
                if num % i == 0 {
                    es_primo = false;
                    break;
                }
            }

            if es_primo {
                primos.push(num);
            }
        }
    }

    // Resultados
    println!("--- Resultados hasta {} ---", n);
    println!("Pares ({}): {:?}", pares.len(), pares);
    println!("Impares ({}): {:?}", impares.len(), impares);
    println!("Primos ({}): {:?}", primos.len(), primos);
}

fn main() {
    clasificar_numeros(20);
}
