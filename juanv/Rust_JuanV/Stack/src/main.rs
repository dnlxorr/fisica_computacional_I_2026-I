#[derive(Debug)]
enum Dato {
    Entero(i32),
    Texto(String),
    Decimal(f64),
    Booleano(bool),
}

// =====================
// PILA (STACK)
// =====================
struct Pila {
    datos: Vec<Dato>,
}

impl Pila {
    fn new() -> Self {
        Pila { datos: Vec::new() }
    }

    fn agregar(&mut self, item: Dato) {
        self.datos.push(item);
    }

    fn quitar(&mut self) -> Option<Dato> {
        self.datos.pop()
    }

    fn cima(&self) -> Option<&Dato> {
        self.datos.last()
    }

    fn vacia(&self) -> bool {
        self.datos.is_empty()
    }
}

// =====================
// COLA (QUEUE)
// =====================
struct Cola {
    datos: Vec<Dato>,
}

impl Cola {
    fn new() -> Self {
        Cola { datos: Vec::new() }
    }

    fn insertar(&mut self, item: Dato) {
        self.datos.push(item);
    }

    fn extraer(&mut self) -> Option<Dato> {
        if self.vacia() {
            None
        } else {
            Some(self.datos.remove(0))
        }
    }

    fn primero(&self) -> Option<&Dato> {
        self.datos.first()
    }

    fn vacia(&self) -> bool {
        self.datos.is_empty()
    }
}

// =====================
// PRUEBAS
// =====================
fn main() {
    // -------- PILA --------
    let mut mi_pila = Pila::new();

    mi_pila.agregar(Dato::Entero(10));
    mi_pila.agregar(Dato::Texto("hola".to_string()));
    mi_pila.agregar(Dato::Decimal(3.14));
    mi_pila.agregar(Dato::Booleano(true));

    println!("Contenido de la pila: {:?}", mi_pila.datos);
    println!("Elemento en la cima: {:?}", mi_pila.cima());

    mi_pila.quitar();
    println!("Después de quitar: {:?}", mi_pila.datos);

    // -------- COLA --------
    let mut mi_cola = Cola::new();

    mi_cola.insertar(Dato::Entero(1));
    mi_cola.insertar(Dato::Texto("mundo".to_string()));
    mi_cola.insertar(Dato::Decimal(2.71));
    mi_cola.insertar(Dato::Booleano(false));

    println!("\nContenido de la cola: {:?}", mi_cola.datos);
    println!("Primer elemento: {:?}", mi_cola.primero());

    mi_cola.extraer();
    println!("Después de extraer: {:?}", mi_cola.datos);
}