import pytest
from utils import run_cmd

def test_tar_present(ssh_client):
    code, out, err = run_cmd(ssh_client, "tar --version")
    assert code == 0, f"tar not available: {err or out}"
    assert "tar" in out.lower()

def test_ln_present(ssh_client):
    code, out, err = run_cmd(ssh_client, "ln --version || (busybox ln --help && echo busybox)")
    assert code == 0 or "busybox" in (out + err).lower(), f"ln not available: {err or out}"

def test_tar_functional_pack_and_unpack(ssh_client):
    cmd = r'''
    set -eu
    TMP_SRC="$(mktemp -d /tmp/smoke_tar_src.XXXXXX)"
    TMP_DST="$(mktemp -d /tmp/smoke_tar_dst.XXXXXX)"
    ARCHIVE="/tmp/smoke_tar_test.tar"

    echo "hello tar" > "${TMP_SRC}/file.txt"

    tar -cf "${ARCHIVE}" -C "${TMP_SRC}" .

    tar -xf "${ARCHIVE}" -C "${TMP_DST}"

    # сравниваем побайтно
    cmp -s "${TMP_SRC}/file.txt" "${TMP_DST}/file.txt"

    # уборка
    rm -rf "${TMP_SRC}" "${TMP_DST}" "${ARCHIVE}"
    '''
    
    code, out, err = run_cmd(ssh_client, cmd)
    assert code == 0, f"tar functional test failed: {err or out}"


def test_ln_functional_symlink_and_hardlink(ssh_client):
    cmd = r'''
    set -eu
    TMP="$(mktemp -d /tmp/smoke_ln.XXXXXX)"
    SRC="${TMP}/src.txt"
    SYM="${TMP}/sym.txt"
    HARD="${TMP}/hard.txt"

    echo "hello ln" > "${SRC}"

    ln -s "${SRC}" "${SYM}"
    
    # symlink существует?
    test -L "${SYM}"
    
    # содержимое совпадает?
    cmp -s "${SRC}" "${SYM}"

    # HARD LINK
    ln "${SRC}" "${HARD}"
    
    # содержимое совпадает?
    cmp -s "${SRC}" "${HARD}"
    
    # количество жёстких ссылок >= 2
    LINKS_COUNT="$(stat -c %h "${SRC}")"
    test "${LINKS_COUNT}" -ge 2

    # уборка
    rm -rf "${TMP}"
    '''
    code, out, err = run_cmd(ssh_client, cmd)
    assert code == 0, f"ln functional test failed: {err or out}"

