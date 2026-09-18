from modelo import Sistema, Solicitud


def registrar_solicitud(sistema):
    id = input("Ingrese el ID de la solicitud: ")
    descripcion = input("Ingrese la descripción: ")

    tipo = input("Ingrese el tipo (Alta/Normal): ").strip().capitalize()

    while tipo != "Alta" and tipo != "Normal":
        print("Tipo inválido.")
        tipo = input("Ingrese el tipo (Alta/Normal): ").strip().capitalize()

    solicitud = Solicitud(id, descripcion, tipo)

    sistema.registrar_solicitud(solicitud)

    print("Solicitud registrada correctamente.")


def eliminar_area(sistema):
    nombre = input("Ingrese el nombre del área a eliminar: ")

    if sistema.eliminar_area(nombre):
        print("Área eliminada correctamente.")
    else:
        print("El área no existe.")


def agregar_area(sistema):
    nombre = input("Ingrese el nombre de la nueva área: ")
    capacidad = int(input("Ingrese la capacidad por turno: "))

    sistema.agregar_area(nombre, capacidad)

    print("Área agregada correctamente.")


def menu():
    sistema = Sistema()

    opcion = ""

    while opcion != "7":
        print()
        print("============== MESA DE AYUDA ==============")
        print("1. Registrar Solicitud")
        print("2. Ejecutar un Turno")
        print("3. Ejecutar Automáticamente")
        print("4. Eliminar un Área")
        print("5. Agregar Nueva Área")
        print("6. Consultar Estado del Sistema")
        print("7. Salir")
        print("============================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_solicitud(sistema)

        elif opcion == "2":
            if sistema.hay_solicitudes():
                sistema.ejecutar_turno()
            else:
                print("No hay solicitudes pendientes.")

        elif opcion == "3":
            if sistema.hay_solicitudes():
                sistema.ejecutar_automaticamente()
            else:
                print("No hay solicitudes pendientes.")

        elif opcion == "4":
            eliminar_area(sistema)

        elif opcion == "5":
            agregar_area(sistema)

        elif opcion == "6":
            sistema.mostrar_estado()

        elif opcion == "7":
            print("Programa finalizado.")

        else:
            print("Opción inválida.")


menu()