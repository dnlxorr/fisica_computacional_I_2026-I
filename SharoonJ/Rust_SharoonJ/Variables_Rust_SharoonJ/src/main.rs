fn main() {

    println!(" TIPOS DE DATOS ");

    // ENTERO (i32)

    let edad: i32 = 21;
    println!("Edad: {}", edad);
    println!("Tipo: i32");
    println!();

    // DECIMAL (f64)

    let altura: f64 = 1.75;
    println!("Altura: {}", altura);
    println!("Tipo: f64");
    println!();

    // "COMPLEJO" (Rust no lo tiene nativo, se simula con tupla)

    let numero_complejo = (2.0, 3.0); // (parte real, parte imaginaria)
    println!("Número complejo: {} + {}i", numero_complejo.0, numero_complejo.1);
    println!("Tipo: (f64, f64)");
    println!();

    // TEXTO (String)

    let mensaje: String = String::from("Hola, estoy aprendiendo Rust");
    println!("Mensaje: {}", mensaje);
    println!("Tipo: String");
    println!();

    // BOOLEANO (bool)

    let es_estudiante: bool = true;
    println!("¿Es estudiante?: {}", es_estudiante);
    println!("Tipo: bool");
    println!();

    // VECTOR (equivalente a lista)

    let mut numeros = vec![1, 2, 3, 4];
    numeros.push(5);
    println!("Lista: {:?}", numeros);
    println!("Tipo: Vec<i32>");
    println!();

    // TUPLA

    let coordenadas = (10, 20);
    println!("Tupla: ({}, {})", coordenadas.0, coordenadas.1);
    println!("Tipo: (i32, i32)");
    println!();

    // DICCIONARIO (HashMap)

    use std::collections::HashMap;

    let mut persona = HashMap::new();
    persona.insert("nombre", "Ana");
    persona.insert("edad", "22");

    println!("Diccionario: {:?}", persona);
    println!("Tipo: HashMap<&str, &str>");
    println!();

    // CONJUNTO (HashSet)

    use std::collections::HashSet;

    let mut valores = HashSet::new();
    valores.insert(1);
    valores.insert(2);
    valores.insert(2); // repetido
    valores.insert(3);

    println!("Conjunto: {:?}", valores);
    println!("Tipo: HashSet<i32>");
    println!();
}