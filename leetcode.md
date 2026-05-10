\### Задача 396 (Daily Question from May, 1st)

Суть решения заключалась в выведении формулы изменения суммы, пописав на листочке и немного подумав, я поняла, что каждый раз она изменяется на сумму всех элементов массива, минус умноженный на n последний элемент. Так, мы просто находим по формуле из задания изначальную сумму и, проходя циклом по всем элементам обратном порядке, ищём максимальную (хотя, кажется, разницы нет в каком порядке).

```



class Solution396 {

&#x20;   fun maxRotateFunction(nums: IntArray): Int {

&#x20;       val n = nums.size

&#x20;       var sum = 0

&#x20;       var init\_sum = 0

&#x20;       var max\_sum = 0

&#x20;       for (i in 0..n - 1) {

&#x20;           sum += nums\[i]

&#x20;           init\_sum += nums\[i] \* i

&#x20;       }



&#x20;       max\_sum = init\_sum



&#x20;       for (j in n - 1 downTo 0) {

&#x20;           init\_sum += sum - nums\[j] \* n

&#x20;           if (init\_sum > max\_sum)

&#x20;               max\_sum = init\_sum

&#x20;       }

&#x20;       return max\_sum

&#x20;   }

}

```

