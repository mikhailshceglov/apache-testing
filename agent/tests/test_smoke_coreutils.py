from conftest import run_cmd

def _ok(code, out, err, msg):
    assert code == 0, f"{msg}\nexit={code}\nstdout:\n{out}\nstderr:\n{err}"


def test_tar_present(ssh_client):
    code, out, err = run_cmd(ssh_client, "tar --version")
    _ok(code, out, err, "tar отсутствует или не запускается")


def test_ln_present(ssh_client):
    code, out, err = run_cmd(ssh_client, "ln --version")
    _ok(code, out, err, "ln отсутствует или не запускается")


def test_tar_functional_pack_and_unpack(ssh_client):
    code, src, err = run_cmd(ssh_client, 'mktemp -d /tmp/smoke_tar_src.XXXXXX')
    _ok(code, src, err, "mktemp src не создал директорию")
    src = src.strip()

    code, dst, err = run_cmd(ssh_client, 'mktemp -d /tmp/smoke_tar_dst.XXXXXX')
    _ok(code, dst, err, "mktemp dst не создал директорию")
    dst = dst.strip()

    archive = "/tmp/smoke_tar_test.tar"

    # создаём файл-образец
    code, out, err = run_cmd(ssh_client, f'echo "hello tar" > "{src}/file.txt"')
    _ok(code, out, err, "не смогли создать файл-образец")

    # упаковка
    code, out, err = run_cmd(ssh_client, f'tar -cf "{archive}" -C "{src}" .')
    _ok(code, out, err, "ошибка при tar -cf")

    # распаковка
    code, out, err = run_cmd(ssh_client, f'tar -xf "{archive}" -C "{dst}"')
    _ok(code, out, err, "ошибка при tar -xf")

    # сравнение
    code, out, err = run_cmd(ssh_client, f'cmp -s "{src}/file.txt" "{dst}/file.txt"')
    _ok(code, out, err, "распакованный файл отличается от исходного")

    run_cmd(ssh_client, f'rm -rf "{src}" "{dst}" "{archive}"')


def test_ln_functional_symlink_and_hardlink(ssh_client):
    code, tmp, err = run_cmd(ssh_client, 'mktemp -d /tmp/smoke_ln.XXXXXX')
    _ok(code, tmp, err, "mktemp не создал рабочую директорию")
    tmp = tmp.strip()

    src = f"{tmp}/src.txt"
    sym = f"{tmp}/sym.txt"
    hard = f"{tmp}/hard.txt"

    # исходный файл
    code, out, err = run_cmd(ssh_client, f'echo "hello ln" > "{src}"')
    _ok(code, out, err, "не смогли создать исходный файл")

    # символьная ссылка
    code, out, err = run_cmd(ssh_client, f'ln -s "{src}" "{sym}"')
    _ok(code, out, err, "ошибка ln -s (символическая ссылка)")

    code, out, err = run_cmd(ssh_client, f'test -L "{sym}"')
    _ok(code, out, err, "символическая ссылка не распознана")

    code, out, err = run_cmd(ssh_client, f'cmp -s "{src}" "{sym}"')
    _ok(code, out, err, "символическая ссылка указывает хз куда")

    # жёсткая ссылка
    code, out, err = run_cmd(ssh_client, f'ln "{src}" "{hard}"')
    _ok(code, out, err, "ошибка ln (жёсткая ссылка)")

    # контент совпадает
    code, out, err = run_cmd(ssh_client, f'cmp -s "{src}" "{hard}"')
    _ok(code, out, err, "жёсткая ссылка указывает не на идентичный контент")

    # кол-во жёстких ссылок >= 2
    code, links, err = run_cmd(ssh_client, f'stat -c %h "{src}"')
    _ok(code, links, err, "stat не отработал")
    assert int(links.strip()) >= 2, f"ожидали >=2 жёстких ссылок, получили: {links}"

    run_cmd(ssh_client, f'rm -rf "{tmp}"')
