# TDD Protocol (`.project/rules/40-testing/tdd-protocol.md`)

## Ciclo Obligatorio
```text
REQUIREMENT -> TEST RED -> IMPLEMENT GREEN -> REFACTOR -> VERIFY -> DONE
```

1. **TEST RED:** Escribir una prueba unitaria o de integración que exprese el requisito y ejecutarla verificando que falla por la causa esperada.
2. **IMPLEMENT GREEN:** Escribir el código mínimo necesario para satisfacer la prueba.
3. **REFACTOR:** Mejorar diseño, tipado y legibilidad manteniendo todas las pruebas en verde.
4. **VERIFY:** Ejecutar la suite completa y registrar el paso en `.engine/harness.py`.
5. **Detección de Tests Falsos:** Se prohíben pruebas vacías, aserciones triviales (`assert True`) o mocks que reproduzcan la implementación sin validar el contrato.
