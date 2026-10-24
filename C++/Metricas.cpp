#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <fstream>

struct Stats {
    long long comparaciones = 0;
    long long intercambios = 0;
    void reset() { comparaciones = 0; intercambios = 0; }
};

std::vector<int> bubbleSort(const std::vector<int>& arr, Stats& s) {
    std::vector<int> a = arr;
    int n = a.size();
    for (int i = 0; i < n; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            s.comparaciones++;
            if (a[j] > a[j + 1]) {
                std::swap(a[j], a[j + 1]);
                s.intercambios++;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return a;
}

std::vector<int> selectionSort(const std::vector<int>& arr, Stats& s) {
    std::vector<int> a = arr;
    int n = a.size();
    for (int i = 0; i < n; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            s.comparaciones++;
            if (a[j] < a[min_idx]) min_idx = j;
        }
        if (min_idx != i) {
            std::swap(a[i], a[min_idx]);
            s.intercambios++;
        }
    }
    return a;
}

std::vector<int> insertionSort(const std::vector<int>& arr, Stats& s) {
    std::vector<int> a = arr;
    for (size_t i = 1; i < a.size(); i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0) {
            s.comparaciones++;
            if (a[j] > key) {
                a[j + 1] = a[j];
                s.intercambios++;
                j--;
            } else { break; }
        }
        a[j + 1] = key;
    }
    return a;
}

std::vector<int> merge(const std::vector<int>& left, const std::vector<int>& right, Stats& s) {
    std::vector<int> merged;
    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        s.comparaciones++;
        if (left[i] <= right[j]) merged.push_back(left[i++]);
        else merged.push_back(right[j++]);
        s.intercambios++;
    }
    while (i < left.size()) { merged.push_back(left[i++]); s.intercambios++; }
    while (j < right.size()) { merged.push_back(right[j++]); s.intercambios++; }
    return merged;
}

std::vector<int> mergeSort(const std::vector<int>& arr, Stats& s) {
    if (arr.size() <= 1) return arr;
    size_t mid = arr.size() / 2;
    std::vector<int> left(arr.begin(), arr.begin() + mid);
    std::vector<int> right(arr.begin() + mid, arr.end());
    return merge(mergeSort(left, s), mergeSort(right, s), s);
}

int partition(std::vector<int>& a, int low, int high, Stats& s) {
    int pivot = a[high], i = low - 1;
    for (int j = low; j < high; j++) {
        s.comparaciones++;
        if (a[j] <= pivot) {
            i++;
            std::swap(a[i], a[j]);
            s.intercambios++;
        }
    }
    std::swap(a[i + 1], a[high]);
    s.intercambios++;
    return i + 1;
}

void quickSortRec(std::vector<int>& a, int low, int high, Stats& s) {
    if (low < high) {
        int pi = partition(a, low, high, s);
        quickSortRec(a, low, pi - 1, s);
        quickSortRec(a, pi + 1, high, s);
    }
}

std::vector<int> quickSort(const std::vector<int>& arr, Stats& s) {
    std::vector<int> a = arr;
    quickSortRec(a, 0, a.size() - 1, s);
    return a;
}

void heapify(std::vector<int>& arr, int n, int i, Stats& s) {
    int largest = i, l = 2 * i + 1, r = 2 * i + 2;
    if (l < n) { s.comparaciones++; if (arr[l] > arr[largest]) largest = l; }
    if (r < n) { s.comparaciones++; if (arr[r] > arr[largest]) largest = r; }
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        s.intercambios++;
        heapify(arr, n, largest, s);
    }
}

std::vector<int> heapSort(const std::vector<int>& arr, Stats& s) {
    std::vector<int> a = arr;
    int n = a.size();
    for (int i = n / 2 - 1; i >= 0; i--) heapify(a, n, i, s);
    for (int i = n - 1; i > 0; i--) {
        std::swap(a[0], a[i]);
        s.intercambios++;
        heapify(a, i, 0, s);
    }
    return a;
}

std::vector<int> countingSort(const std::vector<int>& arr, Stats& s) {
    if (arr.empty()) return {};
    int min_v = *std::min_element(arr.begin(), arr.end());
    int max_v = *std::max_element(arr.begin(), arr.end());
    int range = max_v - min_v + 1;
    std::vector<int> count(range, 0);
    for (int num : arr) count[num - min_v]++;
    std::vector<int> output(arr.size());
    int idx = 0;
    for (int i = 0; i < range; i++) {
        while (count[i] > 0) {
            output[idx++] = i + min_v;
            s.intercambios++;
            count[i]--;
        }
    }
    return output;
}

std::vector<int> bucketSort(const std::vector<int>& arr, Stats& s) {
    if (arr.empty()) return {};
    int min_v = *std::min_element(arr.begin(), arr.end());
    int max_v = *std::max_element(arr.begin(), arr.end());
    if (min_v == max_v) return arr;
    std::vector<std::vector<int>> buckets(10);
    for (int num : arr) {
        s.comparaciones++;
        int idx = 10 * (num - min_v) / (max_v - min_v + 1);
        buckets[std::min(idx, 9)].push_back(num);
    }
    std::vector<int> output;
    for (auto& b : buckets) {
        std::vector<int> sortedB = insertionSort(b, s);
        output.insert(output.end(), sortedB.begin(), sortedB.end());
        s.intercambios += sortedB.size();
    }
    return output;
}

std::vector<int> countingRadix(const std::vector<int>& arr, int exp, Stats& s) {
    int n = arr.size();
    std::vector<int> output(n);
    std::vector<int> count(10, 0);
    for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
    for (int i = 1; i < 10; i++) count[i] += count[i - 1];
    for (int i = n - 1; i >= 0; i--) {
        int idx = (arr[i] / exp) % 10;
        output[count[idx] - 1] = arr[i];
        s.intercambios++;
        count[idx]--;
    }
    return output;
}

std::vector<int> radixSort(const std::vector<int>& arr, Stats& s) {
    if (arr.empty()) return {};
    int min_v = *std::min_element(arr.begin(), arr.end());
    int shift = min_v < 0 ? std::abs(min_v) : 0;
    std::vector<int> a = arr;
    for (int& x : a) x += shift;
    int max_v = *std::max_element(a.begin(), a.end());
    int exp = 1;
    while (max_v / exp > 0) {
        a = countingRadix(a, exp, s);
        exp *= 10;
    }
    for (int& x : a) x -= shift;
    return a;
}

int main() {
    std::vector<int> tamanos = {100, 1000, 10000, 100000, 1000000};
    std::vector<std::string> estados = {"aleatorio", "ordenado", "inverso"};
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100000);
    Stats stats;

    std::ofstream file("resultados_cpp.json");
    if (!file.is_open()) return 1;

    file << "[\n";
    bool first = true;

    for (int size : tamanos) {
        std::vector<int> base(size);
        for (int i = 0; i < size; ++i) base[i] = dis(gen);

        for (const auto& estado : estados) {
            std::vector<int> arr = base;
            if (estado == "ordenado") std::sort(arr.begin(), arr.end());
            else if (estado == "inverso") std::sort(arr.begin(), arr.end(), std::greater<int>());

            std::vector<std::pair<std::string, std::vector<int> (*)(const std::vector<int>&, Stats&)>> algoritmos = {
                {"BubbleSort", bubbleSort}, {"SelectionSort", selectionSort},
                {"InsertionSort", insertionSort}, {"MergeSort", mergeSort},
                {"QuickSort", quickSort}, {"HeapSort", heapSort},
                {"HashSort", countingSort}, {"BucketSort", bucketSort},
                {"RadixSort", radixSort}
            };

            for (auto& alg : algoritmos) {
                if (size >= 100000 && (alg.first == "BubbleSort" || alg.first == "SelectionSort" || alg.first == "InsertionSort")) continue;
                stats.reset();
                auto t0 = std::chrono::high_resolution_clock::now();
                alg.second(arr, stats);
                auto t1 = std::chrono::high_resolution_clock::now();
                double t_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

                if (!first) file << ",\n";
                file << "  {\n"
                    << "    \"lenguaje\": \"C++\",\n"
                    << "    \"algoritmo\": \"" << alg.first << "\",\n"
                    << "    \"tamano\": " << size << ",\n"
                    << "    \"estado\": \"" << estado << "\",\n"
                    << "    \"tiempo_ms\": " << t_ms << ",\n"
                    << "    \"comparaciones\": " << stats.comparaciones << ",\n"
                    << "    \"intercambios\": " << stats.intercambios << "\n"
                    << "  }";
                file.flush();
                first = false;
                std::cout << "C++ | " << alg.first << " | " << size << " | " << estado << " -> Hecho\n";
            }
        }
    }
    file << "\n]";
    file.close();
    std::cout << "¡Archivo resultados_cpp.json guardado con éxito!\n";
    return 0;
}