### Задача 396 (Daily Question from May, 1st)
Суть решения заключалась в выведении формулы изменения суммы, пописав на листочке и немного подумав, я поняла, что каждый раз она изменяется на сумму всех элементов массива, минус умноженный на n последний элемент. Так, мы просто находим по формуле из задания изначальную сумму и, проходя циклом по всем элементам обратном порядке, ищём максимальную (хотя, кажется, разницы нет в каком порядке).
```

class Solution396 {
    fun maxRotateFunction(nums: IntArray): Int {
        val n = nums.size
        var sum = 0
        var init_sum = 0
        var max_sum = 0
        for (i in 0..n - 1) {
            sum += nums[i]
            init_sum += nums[i] * i
        }

        max_sum = init_sum

        for (j in n - 1 downTo 0) {
            init_sum += sum - nums[j] * n
            if (init_sum > max_sum)
                max_sum = init_sum
        }
        return max_sum
    }
}
```
