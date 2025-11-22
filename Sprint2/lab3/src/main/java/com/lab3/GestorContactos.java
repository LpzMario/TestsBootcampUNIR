package com.lab3;

import java.util.ArrayList;
import java.util.List;

public class GestorContactos {
    
    private ArrayList<Contacto> contactos;
    
    public GestorContactos() {
        this.contactos = new ArrayList<>();
    }
    
    public void agregarContacto(Contacto contacto) {
        // No agregar si ya existe un contacto con el mismo ID
        if (buscarContactoPorId(contacto.getId()) == null) {
            contactos.add(contacto);
        }
    }
    
    public Contacto buscarContactoPorId(int id) {
        for (Contacto contacto : contactos) {
            if (contacto.getId() == id) {
                return contacto;
            }
        }
        return null;
    }
    
    public boolean eliminarContacto(int id) {
        Contacto contacto = buscarContactoPorId(id);
        if (contacto != null) {
            contactos.remove(contacto);
            return true;
        }
        return false;
    }
    
    public List<Contacto> obtenerTodosLosContactos() {
        return new ArrayList<>(contactos);
    }
}