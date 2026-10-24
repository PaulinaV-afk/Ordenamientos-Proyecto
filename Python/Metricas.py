import json
import time
import random
import sys

sys.setrecursionlimit(2000000)

class Stats:
    def __init__(self):
        self.comparaciones = 0
        self.intercambios = 0
    def reset(self):
        self.comparaciones = 0
        self.intercambios = 0

# 1. BUBBLE SORT
def bubble_sort(arr, s):
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            s.comparaciones += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                s.intercambios += 1
                swapped = True
        if not swapped: break
    return a

# 2. SELECTION SORT
def selection_sort(arr, s):
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            s.comparaciones += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            s.intercambios += 1
    return a

# 3. INSERTION SORT
def insertion_sort(arr, s):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            s.comparaciones += 1
            if a[j] > key:
                a[j + 1] = a[j]
                s.intercambios += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a

# 4. MERGE SORT
def merge_sort(arr, s):
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], s)
    right = merge_sort(arr[mid:], s)
    
    return merge(left, right, s)

def merge(left, right, s):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        s.comparaciones += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        s.intercambios += 1 # Contabilizamos la reubicación de elementos
    while i < len(left):
        merged.append(left[i])
        i += 1
        s.intercambios += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
        s.intercambios += 1
    return merged

# 5. QUICK SORT
def quick_sort(arr, s):
    a = list(arr)
    _quick_sort_rec(a, 0, len(a) - 1, s)
    return a

def _quick_sort_rec(a, low, high, s):
    if low < high:
        pi = _partition(a, low, high, s)
        _quick_sort_rec(a, low, pi - 1, s)
        _quick_sort_rec(a, pi + 1, high, s)

def _partition(a, low, high, s):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        s.comparaciones += 1
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
            s.intercambios += 1
    a[i + 1], a[high] = a[high], a[i + 1]
    s.intercambios += 1
    return i + 1

# 6. HEAP SORT
def heapify(arr, n, i, s):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n:
        s.comparaciones += 1
        if arr[l] > arr[largest]: largest = l
    if r < n:
        s.comparaciones += 1
        if arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        s.intercambios += 1
        heapify(arr, n, largest, s)

def heap_sort(arr, s):
    a = list(arr)
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i, s)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        s.intercambios += 1
        heapify(a, i, 0, s)
    return a

# 7. HASH / COUNTING SORT
def counting_sort(arr, s):
    if not arr: return []
    a = list(arr)
    min_v, max_v = min(a), max(a)
    range_v = max_v - min_v + 1
    count = [0] * range_v
    output = [0] * len(a)
    for val in a: count[val - min_v] += 1
    idx = 0
    for i in range(range_v):
        while count[i] > 0:
            output[idx] = i + min_v
            s.intercambios += 1
            idx += 1
            count[i] -= 1
    return output

# 8. BUCKET SORT
def bucket_sort(arr, s):
    if not arr: return []
    a = list(arr)
    min_v, max_v = min(a), max(a)
    if min_v == max_v: return a
    buckets = [[] for _ in range(10)]
    for num in a:
        s.comparaciones += 1
        idx = int(10 * (num - min_v) / (max_v - min_v + 1))
        buckets[min(idx, 9)].append(num)
    output = []
    for b in buckets:
        sorted_b = insertion_sort(b, s)
        output.extend(sorted_b)
        s.intercambios += len(sorted_b)
    return output

# 9. RADIX SORT
def counting_radix(arr, exp, s):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        idx = (arr[i] // exp) % 10
        count[idx] += 1
    for i in range(1, 10): count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        idx = (arr[i] // exp) % 10
        output[count[idx] - 1] = arr[i]
        s.intercambios += 1
        count[idx] -= 1
        i -= 1
    return output

def radix_sort(arr, s):
    if not arr: return []
    a = list(arr)
    min_v = min(a)
    shift = abs(min_v) if min_v < 0 else 0
    a = [x + shift for x in a]
    max_v = max(a)
    exp = 1
    while max_v // exp > 0:
        a = counting_radix(a, exp, s)
        exp *= 10
    return [x - shift for x in a]

def main():
    tamanos = [100, 1000, 10000, 100000, 1000000]
    estados = ["aleatorio", "ordenado", "inverso"]
    algoritmos = [
        ("BubbleSort", bubble_sort), ("SelectionSort", selection_sort),
        ("InsertionSort", insertion_sort), ("MergeSort", merge_sort),
        ("QuickSort", quick_sort), ("HeapSort", heap_sort),
        ("HashSort", counting_sort), ("BucketSort", bucket_sort),
        ("RadixSort", radix_sort)
    ]
    resultados = []
    stats = Stats()
    
    for size in tamanos:
        base = [random.randint(0, 100000) for _ in range(size)]
        for estado in estados:
            if estado == "aleatorio": arr = list(base)
            elif estado == "ordenado": arr = sorted(base)
            else: arr = sorted(base, reverse=True)
            
            for nombre, func in algoritmos:
                # Omitir algoritmos O(N^2) en tamaños grandes para optimizar tiempo
                if size >= 100000 and nombre in ["BubbleSort", "SelectionSort", "InsertionSort"]: 
                    continue
                
                stats.reset()
                t0 = time.perf_counter()
                func(arr, stats)
                t1 = time.perf_counter()
                
                resultados.append({
                    "lenguaje": "Python", 
                    "algoritmo": nombre, 
                    "tamano": size,
                    "estado": estado, 
                    "tiempo_ms": round((t1 - t0) * 1000, 4),
                    "comparaciones": stats.comparaciones, 
                    "intercambios": stats.intercambios
                })
                print(f"Python | {nombre} | Tamaño: {size} | Estado: {estado} -> Hecho")
                
    with open("resultados_python.json", "w") as f:
        json.dump(resultados, f, indent=4)
    print("\n¡Archivo resultados_python.json guardado con éxito!")

if __name__ == "__main__":
    main()