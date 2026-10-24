import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Benchmark {
    static class Stats {
        long comparaciones = 0;
        long intercambios = 0;
        void reset() { comparaciones = 0; intercambios = 0; }
    }

    static int[] bubbleSort(int[] arr, Stats s) {
        int[] a = arr.clone();
        int n = a.length;
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
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

    static int[] selectionSort(int[] arr, Stats s) {
        int[] a = arr.clone();
        int n = a.length;
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

    static int[] insertionSort(int[] arr, Stats s) {
        int[] a = arr.clone();
        for (int i = 1; i < a.length; i++) {
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

    static int[] merge(int[] left, int[] right, Stats s) {
        int[] merged = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            s.comparaciones++;
            if (left[i] <= right[j]) merged[k++] = left[i++];
            else merged[k++] = right[j++];
            s.intercambios++;
        }
        while (i < left.length) { merged[k++] = left[i++]; s.intercambios++; }
        while (j < right.length) { merged[k++] = right[j++]; s.intercambios++; }
        return merged;
    }

    static int[] mergeSort(int[] arr, Stats s) {
        if (arr.length <= 1) return arr.clone();
        int mid = arr.length / 2;
        int[] left = mergeSort(Arrays.copyOfRange(arr, 0, mid), s);
        int[] right = mergeSort(Arrays.copyOfRange(arr, mid, arr.length), s);
        return merge(left, right, s);
    }

    static int partition(int[] a, int low, int high, Stats s) {
        int pivot = a[high], i = low - 1;
        for (int j = low; j < high; j++) {
            s.comparaciones++;
            if (a[j] <= pivot) {
                i++;
                int t = a[i]; a[i] = a[j]; a[j] = t;
                s.intercambios++;
            }
        }
        int t = a[i + 1]; a[i + 1] = a[high]; a[high] = t;
        s.intercambios++;
        return i + 1;
    }

    static void quickSortRec(int[] a, int low, int high, Stats s) {
        if (low < high) {
            int pi = partition(a, low, high, s);
            quickSortRec(a, low, pi - 1, s);
            quickSortRec(a, pi + 1, high, s);
        }
    }

    static int[] quickSort(int[] arr, Stats s) {
        int[] a = arr.clone();
        quickSortRec(a, 0, a.length - 1, s);
        return a;
    }

    static void heapify(int[] arr, int n, int i, Stats s) {
        int largest = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n) { s.comparaciones++; if (arr[l] > arr[largest]) largest = l; }
        if (r < n) { s.comparaciones++; if (arr[r] > arr[largest]) largest = r; }
        if (largest != i) {
            int t = arr[i]; arr[i] = arr[largest]; arr[largest] = t;
            s.intercambios++; heapify(arr, n, largest, s);
        }
    }

    static int[] heapSort(int[] arr, Stats s) {
        int[] a = arr.clone();
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(a, n, i, s);
        for (int i = n - 1; i > 0; i--) {
            int t = a[0]; a[0] = a[i]; a[i] = t; s.intercambios++;
            heapify(a, i, 0, s);
        }
        return a;
    }

    static int[] countingSort(int[] arr, Stats s) {
        if (arr.length == 0) return new int[0];
        int min = Arrays.stream(arr).min().getAsInt();
        int max = Arrays.stream(arr).max().getAsInt();
        int range = max - min + 1;
        int[] count = new int[range];
        for (int num : arr) count[num - min]++;
        int[] output = new int[arr.length];
        int idx = 0;
        for (int i = 0; i < range; i++) {
            while (count[i] > 0) {
                output[idx++] = i + min; s.intercambios++; count[i]--;
            }
        }
        return output;
    }

    static int[] bucketSort(int[] arr, Stats s) {
        if (arr.length == 0) return new int[0];
        int min = Arrays.stream(arr).min().getAsInt();
        int max = Arrays.stream(arr).max().getAsInt();
        if (min == max) return arr.clone();
        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new ArrayList[10];
        for (int i = 0; i < 10; i++) buckets[i] = new ArrayList<>();
        for (int num : arr) {
            s.comparaciones++;
            int idx = (int) (10.0 * (num - min) / (max - min + 1));
            buckets[Math.min(idx, 9)].add(num);
        }
        int[] output = new int[arr.length];
        int idx = 0;
        for (List<Integer> b : buckets) {
            int[] bArr = b.stream().mapToInt(i -> i).toArray();
            int[] sortedB = insertionSort(bArr, s);
            System.arraycopy(sortedB, 0, output, idx, sortedB.length);
            idx += sortedB.length;
            s.intercambios += sortedB.length;
        }
        return output;
    }

    static int[] countingRadix(int[] arr, int exp, Stats s) {
        int n = arr.length;
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

    static int[] radixSort(int[] arr, Stats s) {
        if (arr.length == 0) return new int[0];
        int min = Arrays.stream(arr).min().getAsInt();
        int shift = min < 0 ? Math.abs(min) : 0;
        int[] a = Arrays.stream(arr).map(x -> x + shift).toArray();
        int max = Arrays.stream(a).max().getAsInt();
        int exp = 1;
        while (max / exp > 0) {
            a = countingRadix(a, exp, s);
            exp *= 10;
        }
        return Arrays.stream(a).map(x -> x - shift).toArray();
    }

    public static void main(String[] args) {
        int[] tamanos = {100, 1000, 10000, 100000, 1000000};
        String[] estados = {"aleatorio", "ordenado", "inverso"};
        Random rand = new Random();
        Stats stats = new Stats();
        StringBuilder json = new StringBuilder("[\n");
        boolean first = true;

        for (int size : tamanos) {
            int[] base = rand.ints(size, 0, 100000).toArray();
            for (String estado : estados) {
                int[] arr = base.clone();
                Arrays.sort(arr);
                if (estado.equals("inverso")) {
                    for (int i = 0; i < arr.length / 2; i++) {
                        int temp = arr[i]; arr[i] = arr[arr.length - 1 - i]; arr[arr.length - 1 - i] = temp;
                    }
                } else if (estado.equals("aleatorio")) {
                    arr = base.clone();
                }

                String[] algoritmos = {"BubbleSort", "SelectionSort", "InsertionSort", "MergeSort", "QuickSort", "HeapSort", "HashSort", "BucketSort", "RadixSort"};

                for (String nombre : algoritmos) {
                    if (size >= 100000 && (nombre.equals("BubbleSort") || nombre.equals("SelectionSort") || nombre.equals("InsertionSort"))) continue;
                    stats.reset();
                    long t0 = System.nanoTime();
                    
                    switch (nombre) {
                        case "BubbleSort": bubbleSort(arr, stats); break;
                        case "SelectionSort": selectionSort(arr, stats); break;
                        case "InsertionSort": insertionSort(arr, stats); break;
                        case "MergeSort": mergeSort(arr, stats); break;
                        case "QuickSort": quickSort(arr, stats); break;
                        case "HeapSort": heapSort(arr, stats); break;
                        case "HashSort": countingSort(arr, stats); break;
                        case "BucketSort": bucketSort(arr, stats); break;
                        case "RadixSort": radixSort(arr, stats); break;
                    }
                    long t1 = System.nanoTime();
                    double tiempoMs = (t1 - t0) / 1_000_000.0;

                    if (!first) json.append(",\n");
                    json.append(String.format(Locale.US, 
                        "  {\n    \"lenguaje\": \"Java\",\n    \"algoritmo\": \"%s\",\n    \"tamano\": %d,\n    \"estado\": \"%s\",\n    \"tiempo_ms\": %.4f,\n    \"comparaciones\": %d,\n    \"intercambios\": %d\n  }",
                        nombre, size, estado, tiempoMs, stats.comparaciones, stats.intercambios));
                    first = false;
                    System.out.println("Java | " + nombre + " | " + size + " | " + estado + " -> Hecho");
                }
            }
        }
        json.append("\n]");
        try (FileWriter file = new FileWriter("resultados_java.json")) {
            file.write(json.toString());
            System.out.println("¡Archivo resultados_java.json guardado con éxito!");
        } catch (IOException e) { e.printStackTrace(); }
    }
}