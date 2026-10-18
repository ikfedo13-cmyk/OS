#!/bin/bash
# Construye la ISO. Debe ejecutarse en Debian 13 con permisos de administrador.
set -uo pipefail
export DEBIAN_FRONTEND=noninteractive

# Activar contrib y non-free-firmware para que existan los paquetes de firmware
echo "deb http://deb.debian.org/debian trixie main contrib non-free-firmware" > /etc/apt/sources.list.d/litenova.list
apt-get update
apt-get install -y live-build debootstrap python3-pil python3-numpy ca-certificates

python3 tools/make_wallpapers.py || exit 1

# Quitar de la lista los paquetes que no existan (así un nombre erróneo no rompe toda la build)
LIST=config/package-lists/litenova.list.chroot
: > build-skipped.txt
grep -v '^#' "$LIST" | grep -v '^$' | while read -r p; do
  if ! apt-cache show "$p" >/dev/null 2>&1; then
    echo "$p" >> build-skipped.txt
    sed -i "/^$p\$/d" "$LIST"
  fi
done
echo "Paquetes omitidos por no existir:"; cat build-skipped.txt

lb clean --purge || true
lb config || exit 1
lb build 2>&1 | tee build.log
if [ "${PIPESTATUS[0]}" -ne 0 ]; then echo "LA CONSTRUCCION HA FALLADO, revisa build.log"; exit 1; fi

ISO=$(ls -1 *.iso | head -n1)
mv "$ISO" litenova-os-0.1-amd64.iso
sha256sum litenova-os-0.1-amd64.iso > SHA256SUMS
echo "Listo: litenova-os-0.1-amd64.iso"
