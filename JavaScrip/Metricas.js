const fs = require('fs');

class Stats {
    constructor() { this.comparaciones = 0; this.intercambios = 0; }
    reset() { this.comparaciones = 0; this.intercambios = 0; }
}

function bubbleSort(arr, s) {
    let a = [...arr], n = a.length;
    for (let i = 0; i < n; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            s.comparaciones++;
            if (a[j] > a[j + 1]) {
                let t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                s.intercambios++; swapped = true;
            }
        }
        if (!swapped) break;
    }
    return a;
}

function selectionSort(arr, s) {
    let a = [...arr], n = a.length;
    for (let i = 0; i < n; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            s.comparaciones++;
            if (a[j] < a[minIdx]) minIdx = j;
        }
        if (minIdx !== i) {
            let t = a[i]; a[i] = a[minIdx]; a[minIdx] = t;
            s.intercambios++;
        }
    }
    return a;
}

function insertionSort(arr, s) {
    let a = [...arr];
    for (let i = 1; i < a.length; i++) {
        let key = a[i], j = i - 1;
        while (j >= 0) {
            s.comparaciones++;
            if (a[j] > key) {
                a[j + 1] = a[j]; s.intercambios++; j--;
            } else { break; }
        }
        a[j + 1] = key;
    }
    return a;
}

function merge(left, right, s) {
    let merged = [], i = 0, j = 0;
    while (i < left.length && j < right.length) {
        s.comparaciones++;
        if (left[i] <= right[j]) { merged.push(left[i++]); }
        else { merged.push(right[j++]); }
        s.intercambios++;
    }
    while (i < left.length) { merged.push(left[i++]); s.intercambios++; }
    while (j < right.length) { merged.push(right[j++]); s.intercambios++; }
    return merged;
}

function mergeSort(arr, s) {
    if (arr.length <= 1) return [...arr];
    let mid = Math.floor(arr.length / 2);
    let left = mergeSort(arr.slice(0, mid), s);
    let right = mergeSort(arr.slice(mid), s);
    return merge(left, right, s);
}

function partition(a, low, high, s) {
    let pivot = a[high], i = low - 1;
    for (let j = low; j < high; j++) {
        s.comparaciones++;
        if (a[j] <= pivot) {
            i++;
            let t = a[i]; a[i] = a[j]; a[j] = t;
            s.intercambios++;
        }
    }
    let t = a[i + 1]; a[i + 1] = a[high]; a[high] = t;
    s.intercambios++;
    return i + 1;
}

function quickSortRec(a, low, high, s) {
    if (low < high) {
        let pi = partition(a, low, high, s);
        quickSortRec(a, low, pi - 1, s);
        quickSortRec(a, pi + 1, high, s);
    }
}

function quickSort(arr, s) {
    let a = [...arr];
    quickSortRec(a, 0, a.length - 1, s);
    return a;
}

function heapify(arr, n, i, s) {
    let largest = i, l = 2 * i + 1, r = 2 * i + 2;
    if (l < n) { s.comparaciones++; if (arr[l] > arr[largest]) largest = l; }
    if (r < n) { s.comparaciones++; if (arr[r] > arr[largest]) largest = r; }
    if (largest !== i) {
        let t = arr[i]; arr[i] = arr[largest]; arr[largest] = t;
        s.intercambios++; heapify(arr, n, largest, s);
    }
}

function heapSort(arr, s) {
    let a = [...arr], n = a.length;
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) heapify(a, n, i, s);
    for (let i = n - 1; i > 0; i--) {
        let t = a[0]; a[0] = a[i]; a[i] = t; s.intercambios++;
        heapify(a, i, 0, s);
    }
    return a;
}

function countingSort(arr, s) {
    if (arr.length === 0) return [];
    let a = [...arr], min = Math.min(...a), max = Math.max(...a);
    let range = max - min + 1, count = new Array(range).fill(0);
    for (let num of a) count[num - min]++;
    let output = new Array(a.length), idx = 0;
    for (let i = 0; i < range; i++) {
        while (count[i] > 0) {
            output[idx++] = i + min; s.intercambios++; count[i]--;
        }
    }
    return output;
}

function bucketSort(arr, s) {
    if (arr.length === 0) return [];
    let a = [...arr], min = Math.min(...a), max = Math.max(...a);
    if (min === max) return a;
    let buckets = Array.from({ length: 10 }, () => []);
    for (let num of a) {
        s.comparaciones++;
        let idx = Math.floor(10 * (num - min) / (max - min + 1));
        buckets[Math.min(idx, 9)].push(num);
    }
    let output = [];
    for (let b of buckets) {
        let sortedB = insertionSort(b, s);
        output.push(...sortedB);
        s.intercambios += sortedB.length;
    }
    return output;
}

function countingRadix(arr, exp, s) {
    let n = arr.length, output = new Array(n), count = new Array(10).fill(0);
    for (let i = 0; i < n; i++) count[Math.floor(arr[i] / exp) % 10]++;
    for (let i = 1; i < 10; i++) count[i] += count[i - 1];
    for (let i = n - 1; i >= 0; i--) {
        let idx = Math.floor(arr[i] / exp) % 10;
        output[count[idx] - 1] = arr[i]; s.intercambios++; count[idx]--;
    }
    return output;
}

function radixSort(arr, s) {
    if (arr.length === 0) return [];
    let a = [...arr], min = Math.min(...a), shift = min < 0 ? Math.abs(min) : 0;
    a = a.map(x => x + shift);
    let max = Math.max(...a), exp = 1;
    while (Math.floor(max / exp) > 0) {
        a = countingRadix(a, exp, s);
        exp *= 10;
    }
    return a.map(x => x - shift);
}

function runBenchmark() {
    const tamanos = [100, 1000, 10000, 100000, 1000000];
    const estados = ["aleatorio", "ordenado", "inverso"];
    const algoritmos = [
        ["BubbleSort", bubbleSort], ["SelectionSort", selectionSort],
        ["InsertionSort", insertionSort], ["MergeSort", mergeSort],
        ["QuickSort", quickSort], ["HeapSort", heapSort],
        ["HashSort", countingSort], ["BucketSort", bucketSort],
        ["RadixSort", radixSort]
    ];
    let resultados = [], stats = new Stats();

    for (let size of tamanos) {
        let base = Array.from({ length: size }, () => Math.floor(Math.random() * 100000));
        for (let estado of estados) {
            let arr = [...base];
            if (estado === "ordenado") arr.sort((a, b) => a - b);
            else if (estado === "inverso") arr.sort((a, b) => b - a);

            for (let [nombre, func] of algoritmos) {
                if (size >= 100000 && ["BubbleSort", "SelectionSort", "InsertionSort"].includes(nombre)) continue;
                stats.reset();
                let t0 = performance.now();
                func(arr, stats);
                let t1 = performance.now();
                resultados.push({
                    lenguaje: "JavaScript", algoritmo: nombre, tamano: size,
                    estado: estado, tiempo_ms: Number((t1 - t0).toFixed(4)),
                    comparaciones: stats.comparaciones, intercambios: stats.intercambios
                });
                console.log(`JS | ${nombre} | ${size} | ${estado} -> Hecho`);
            }
        }
    }
    fs.writeFileSync("resultados_javascript.json", JSON.stringify(resultados, null, 4));
    console.log("¡Archivo resultados_javascript.json guardado con éxito!");
}

runBenchmark();