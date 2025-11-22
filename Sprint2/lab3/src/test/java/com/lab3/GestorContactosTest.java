package com.lab3;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GestorContactosTest {
    
    private GestorContactos gestor;
    
    @BeforeEach
    public void setUp() {
        gestor = new GestorContactos();
    }
    
    @Test
    public void testAgregarContacto() {
        Contacto contacto = new Contacto(1, "Juan Pérez", "juan@email.com", 30);
        gestor.agregarContacto(contacto);
        
        assertEquals(1, gestor.obtenerTodosLosContactos().size());
        assertEquals(contacto, gestor.buscarContactoPorId(1));
    }
    
    @Test
    public void testBuscarContactoPorId() {
        Contacto contacto1 = new Contacto(1, "Juan Pérez", "juan@email.com", 30);
        Contacto contacto2 = new Contacto(2, "María García", "maria@email.com", 25);
        
        gestor.agregarContacto(contacto1);
        gestor.agregarContacto(contacto2);
        
        Contacto encontrado = gestor.buscarContactoPorId(2);
        assertNotNull(encontrado);
        assertEquals("María García", encontrado.getNombre());
    }
    
    @Test
    public void testBuscarContactoInexistente() {
        Contacto encontrado = gestor.buscarContactoPorId(999);
        assertNull(encontrado);
    }
    
    @Test
    public void testEliminarContacto() {
        Contacto contacto = new Contacto(1, "Juan Pérez", "juan@email.com", 30);
        gestor.agregarContacto(contacto);
        
        assertEquals(1, gestor.obtenerTodosLosContactos().size());
        
        boolean eliminado = gestor.eliminarContacto(1);
        assertTrue(eliminado);
        assertEquals(0, gestor.obtenerTodosLosContactos().size());
    }
    
    @Test
    public void testEliminarContactoInexistente() {
        boolean eliminado = gestor.eliminarContacto(999);
        assertFalse(eliminado);
    }
    
    @Test
    public void testNoAgregarContactoDuplicado() {
        Contacto contacto1 = new Contacto(1, "Juan Pérez", "juan@email.com", 30);
        Contacto contacto2 = new Contacto(1, "Otro Nombre", "otro@email.com", 25);
        
        gestor.agregarContacto(contacto1);
        gestor.agregarContacto(contacto2);
        
        assertEquals(1, gestor.obtenerTodosLosContactos().size());
    }
}