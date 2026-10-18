# LiteNova OS 0.1 (prototipo)
Base: Debian 13 "trixie" (amd64) + XFCE. ISO Live con instalador Calamares.

## Estado real (nada de esto está probado todavía)
- Fondos originales generados por script: hecho (comprobados visualmente).
- Configuración live-build, paquetes, marca y fondos: escrita, **sin ejecutar**.
- Barra de tareas inferior estilo LiteNova, menú de inicio propio, logo e iconos: pendiente.
- Chrome: no va en la ISO (no está en los repositorios de Debian); se ofrecerá desde la tienda si hay versión oficial.
- Word: versión web oficial desde el navegador, o LibreOffice.

## Construir en la nube (sin Linux propio)
1. Crea un repositorio **público** nuevo en GitHub (si es privado, el límite de espacio gratuito no deja guardar la ISO).
2. Sube el contenido de esta carpeta. La construcción empieza sola.
3. Pestaña Actions: espera 30-60 min. Descarga `litenova-os-iso` (ahí está la ISO). Si falla, descarga `registro-build` y envía `build.log`.
4. Comprueba `sha256sum -c SHA256SUMS`.

## Probar sin riesgo
Usa una máquina virtual (VirtualBox/QEMU) con 2 GB de RAM y arranque EFI. No instales en tu ordenador real hasta probarla.
