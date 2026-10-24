using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

class Stats {
    public long comparaciones { get; set; } = 0;
    public long intercambios { get; set; } = 0;
    public void Reset() { comparaciones = 0; intercambios = 0; }
}

class Program {
    static int[] BubbleSort(int[] arr, Stats s) {
        int[] a = (int[])arr.Clone();
        int n = a.Length;
        for (int i = 0; i < n; i++) {
            bool swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                s.comparaciones++;
                if (a[j] > a[j + 1]) {
                    int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                    s.intercambios++; swapped = true;
                }
            }
            if (!swapped) break;
        }
        return a;
    }

    static int[] SelectionSort(int[] arr, Stats s) {
        int[] a = (int[])arr.Clone();
        int n = a.Length;
        for (int i = 0; i < n; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                s.comparaciones++;
                if (a[j] < a[minIdx]) minIdx = j;
            }
            if (minIdx != i) {
                int t = a[i]; a[i] = a[minIdx]; a[minIdx] = t;
                s.intercambios++;
            }
        }
        return a;
    }

    static int[] InsertionSort(int[] arr, Stats s) {
        int[] a = (int[])arr.Clone();
        for (int i = 1; i < a.Length; i++) {
            int key = a[i], j = i - 1;
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

    static int[] Merge(int[] left, int[] right, Stats s) {
        int[] merged = new int[left.Length + right.Length];
        int i = 0, j = 0, k = 0;
        while (i < left.Length && j < right.Length) {
            s.comparaciones++;
            if (left[i] <= right[j]) merged[k++] = left[i++];
            else merged[k++] = right[j++];
            s.intercambios++;
        }
        while (i < left.Length) { merged[k++] = left[i++]; s.intercambios++; }
        while (j < right.Length) { merged[k++] = right[j++]; s.intercambios++; }
        return merged;
    }

    static int[] MergeSort(int[] arr, Stats s) {
        if (arr.Length <= 1) return (int[])arr.Clone();
        int mid = arr.Length / 2;
        int[] left = MergeSort(arr.Take(mid).ToArray(), s);
        int[] right = MergeSort(arr.Skip(mid).ToArray(), s);
        return Merge(left, right, s);
    }

    static int Partition(int[] a, int low, int high, Stats s) {
        int pivot = a[high], i = low - 1;
        for (int j = low; j < high; j++) {
            s.comparaciones++;
            if (a[j] <= pivot) {
                i++;
                int t = a[i]; a[i] = a[j]; a[j] = t;
                s.intercambios++;
            }
        }
        int temp = a[i + 1]; a[i + 1] = a[high]; a[high] = temp;
        s.intercambios++;
        return i + 1;
    }

    static void QuickSortRec(int[] a, int low, int high, Stats s) {
        if (low < high) {
            int pi = Partition(a, low, high, s);
            QuickSortRec(a, low, pi - 1, s);
            QuickSortRec(a, pi + 1, high, s);
        }
    }

    static int[] QuickSort(int[] arr, Stats s) {
        int[] a = (int[])arr.Clone();
        QuickSortRec(a, 0, a.Length - 1, s);
        return a;
    }

    static void Heapify(int[] arr, int n, int i, Stats s) {
        int largest = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n) { s.comparaciones++; if (arr[l] > arr[largest]) largest = l; }
        if (r < n) { s.comparaciones++; if (arr[r] > arr[largest]) largest = r; }
        if (largest != i) {
            int t = arr[i]; arr[i] = arr[largest]; arr[largest] = t;
            s.intercambios++; Heapify(arr, n, largest, s);
        }
    }

    static int[] HeapSort(int[] arr, Stats s) {
        int[] a = (int[])arr.Clone();
        int n = a.Length;
        for (int i = n / 2 - 1; i >= 0; i--) Heapify(a, n, i, s);
        for (int i = n - 1; i > 0; i--) {
            int t = a[0]; a[0] = a[i]; a[i] = t; s.intercambios++;
            Heapify(a, i, 0, s);
        }
        return a;
    }

    static int[] CountingSort(int[] arr, Stats s) {
        if (arr.Length == 0) return new int[0];
        int min = arr.Min(), max = arr.Max();
        int range = max - min + 1;
        int[] count = new int[range];
        foreach (int num in arr) count[num - min]++;
        int[] output = new int[arr.Length];
        int idx = 0;
        for (int i = 0; i < range; i++) {
            while (count[i] > 0) {
                output[idx++] = i + min; s.intercambios++; count[i]--;
            }
        }
        return output;
    }

    static int[] BucketSort(int[] arr, Stats s) {
        if (arr.Length == 0) return new int[0];
        int min = arr.Min(), max = arr.Max();
        if (min == max) return (int[])arr.Clone();
        List<int>[] buckets = new List<int>[10];
        for (int i = 0; i < 10; i++) buckets[i] = new List<int>();
        foreach (int num in arr) {
            s.comparaciones++;
            int idx = (int)(10.0 * (num - min) / (max - min + 1));
            buckets[Math.Min(idx, 9)].Add(num);
        }
        int[] output = new int[arr.Length];
        int outIdx = 0;
        foreach (var b in buckets) {
            int[] sortedB = InsertionSort(b.ToArray(), s);
            Array.Copy(sortedB, 0, output, outIdx, sortedB.Length);
            outIdx += sortedB.Length;
            s.intercambios += sortedB.Length;
        }
        return output;
    }

    static int[] CountingRadix(int[] arr, int exp, Stats s) {
        int n = arr.Length;
        int[] output = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++) count[i] += count[i - 1];
        for (int i = n - 1; i >= 0; i--) {
            int idx = (arr[i] / exp) % 10;
            output[count[idx] - 1] = arr[i]; s.intercambios++; count[idx]--;
        }
        return output;
    }

    static int[] RadixSort(int[] arr, Stats s) {
        if (arr.Length == 0) return new int[0];
        int min = arr.Min();
        int shift = min < 0 ? Math.Abs(min) : 0;
        int[] a = arr.Select(x => x + shift).ToArray();
        int max = a.Max();
        int exp = 1;
        while (max / exp > 0) {
            a = CountingRadix(a, exp, s);
            exp *= 10;
        }
        return a.Select(x => x - shift).ToArray();
    }

    static void Main() {
        int[] tamanos = { 100, 1000, 10000, 100000, 1000000 };
        string[] estados = { "aleatorio", "ordenado", "inverso" };
        Random rand = new Random();
        Stats stats = new Stats();
        var resultados = new List<object>();

        foreach (int size in tamanos) {
            int[] baseArr = Enumerable.Range(0, size).Select(_ => rand.Next(0, 100000)).ToArray();
            foreach (string estado in estados) {
                int[] arr = (int[])baseArr.Clone();
                if (estado == "ordenado") Array.Sort(arr);
                else if (estado == "inverso") { Array.Sort(arr); Array.Reverse(arr); }

                var algoritmos = new Dictionary<string, Func<int[], Stats, int[]>> {
                    { "BubbleSort", BubbleSort }, { "SelectionSort", SelectionSort },
                    { "InsertionSort", InsertionSort }, { "MergeSort", MergeSort },
                    { "QuickSort", QuickSort }, { "HeapSort", HeapSort },
                    { "HashSort", CountingSort }, { "BucketSort", BucketSort },
                    { "RadixSort", RadixSort }
                };

                foreach (var alg in algoritmos) {
                    if (size >= 100000 && (alg.Key == "BubbleSort" || alg.Key == "SelectionSort" || alg.Key == "InsertionSort")) continue;
                    stats.Reset();
                    var watch = System.Diagnostics.Stopwatch.StartNew();
                    alg.Value(arr, stats);
                    watch.Stop();
                    double t_ms = watch.Elapsed.TotalMilliseconds;

                    resultados.Add(new {
                        lenguaje = "C#", algoritmo = alg.Key, tamano = size,
                        estado = estado, tiempo_ms = Math.Round(t_ms, 4),
                        comparaciones = stats.comparaciones, intercambios = stats.intercambios
                    });
                    Console.WriteLine($"C# | {alg.Key} | {size} | {estado} -> Hecho");
                }
            }
        }
        string jsonString = JsonSerializer.Serialize(resultados, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText("resultados_csharp.json", jsonString);
        Console.WriteLine("¡Archivo resultados_csharp.json guardado con éxito!");
    }
}