use std::any::type_name;

fn mostrar_dato<T: std::fmt::Debug>(nombre: &str, valor: &T) {
    println!("{}: {:?}", nombre, valor);
    println!("Tipo: {}", type_name::<T>());
    println!();
}

fn main() {
    println!("TIPOS DE DATOS");

    // ENTERO
    let edad = 21;
    mostrar_dato("Edad", &edad);

    // DECIMAL
    let altura = 1.75;
    mostrar_dato("Altura", &altura);

    // COMPLEJO (usando crate num_complex)
    use num_complex::Complex;
    let numero_complejo = Complex::new(2.0, 3.0);
    mostrar_dato("Número complejo", &numero_complejo);

    // TEXTO
    let mensaje = "Hola, estoy aprendiendo Rust";
    mostrar_dato("Mensaje", &mensaje);

    // BOOLEANO
    let es_estudiante = true;
    mostrar_dato("¿Es estudiante?", &es_estudiante);

    // LISTA (Vector)
    let mut numeros = vec![1, 2, 3, 4];
    numeros.push(5);
    mostrar_dato("Lista", &numeros);

    // TUPLA
    let coordenadas = (10, 20);
    mostrar_dato("Tupla", &coordenadas);

    // DICCIONARIO (HashMap)
    use std::collections::HashMap;
    let mut persona = HashMap::new();
    persona.insert("nombre", "Ana");
    persona.insert("edad", "22");
    mostrar_dato("Diccionario", &persona);

    // CONJUNTO (HashSet)
    use std::collections::HashSet;
    let mut valores = HashSet::new();
    valores.insert(1);
    valores.insert(2);
    valores.insert(2);
    valores.insert(3);
    mostrar_dato("Conjunto", &valores);
}