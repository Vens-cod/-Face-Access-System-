# test_storage.py
import threading
import os
import json
from storage import JsonEmployeeStore


def test_file_not_exist():
    """
    测试：⽂件不存在时返回空字典
    """

    if os.path.exists('not_exist.json'):
        os.remove('not_exist.json')
    store = JsonEmployeeStore('not_exist.json')
    result = store.load()
    assert result == {}, "⽂件不存在时应返回空字典"
    print("✅测试通过：⽂件不存在")


def test_empty_file():
    """
    测试：空⽂件返回空字典
    """

    with open('empty.json', 'w') as f:
        f.write('')
    store = JsonEmployeeStore('empty.json')
    result = store.load()
    assert result == {}, "空⽂件应返回空字典"
    os.remove('empty.json')
    print("✅测试通过：空⽂件")


def test_corrupted_file():
    """
    测试：损坏⽂件处理
    """

    with open('corrupt.json', 'w') as f:
        f.write('not valid json{')
    store = JsonEmployeeStore('corrupt.json')
    result = store.load()
    assert result == {}, "损坏⽂件应返回空字典"
    os.remove('corrupt.json')
    print("✅测试通过：损坏⽂件")


def test_concurrent_write():
    """
    测试：多线程并发写⼊
    """

    store = JsonEmployeeStore('concurrent.json')

    def worker(n):
        data = store.load()

        data[f'EMP{n}'] = {'name': f'员⼯{n}'}
        store.save(data)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    result = store.load()
    assert len(result) == 10, f"应有10条记录，实际{len(result)}条"
    os.remove('concurrent.json')
    print("✅测试通过：多线程并发")


if __name__ == '__main__':
    test_file_not_exist()
    test_empty_file()
    test_corrupted_file()
    test_concurrent_write()
    print("\n🎉所有测试通过！")
