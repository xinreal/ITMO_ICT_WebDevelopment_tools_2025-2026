### [Задача 396 (Daily Question from May, 1st)](https://leetcode.com/problems/rotate-function/description/?envType=daily-question&envId=2026-05-01)
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

### [Задача 796 (Daily Question from May, 3rd)](https://leetcode.com/problems/rotate-string/description/?envType=daily-question&envId=2026-05-03)
В этой задаче я просто удвоила строку s, тем самым получив строку которая содержит в себе все возможные s полученные сдвигом и потом я ищу в ней goal.

```
class Solution796 {
    fun rotateString(s: String, goal: String): Boolean {
        val checkString = s + s
        return (checkString.contains(goal) && s.length == goal.length)
    }
}
```

### [Задача 1665 (Daily Question from May, 12th)](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/description/?envType=daily-question&envId=2026-05-12)
В каком бы порядке мы ни выполняли задачи, сумма реально затраченной энергии останется одинаковой. Перед каждой задачей у нас должен быть запас не меньше `minimum`, если задачу с большим `minimum - actual` оставить на потом, то к этому моменту мы уже потеряем часть энергии на предыдущих задачах, и изначально придётся брать больше энергии.
Поэтому задачи с большой разницей `minimum - actual` выгодно выполнять раньше: они требуют высокий запас на входе, но после выполнения оставляют относительно много энергии для следующих задач. Так мы уменьшаем максимальный стартовый запас, который вообще понадобится для решения всех задач.

```
class Solution1665 {
    fun minimumEffort(tasks: Array<IntArray>): Int {
        tasks.sortByDescending { it[1] - it[0] }

        var minEnergy = 0
        var currentEnergy = 0

        for (task in tasks) {
            val actual = task[0]
            val minimum = task[1]

            if (currentEnergy < minimum) {
                val lack = minimum - currentEnergy
                minEnergy += lack
                currentEnergy += lack
            }

            currentEnergy -= actual
        }

        return minEnergy
    }
}
```
### [Задача 2553 (Daily Question from May, 11th)](https://leetcode.com/problems/separate-the-digits-in-an-array/description/?envType=daily-question&envId=2026-05-11)
Каждое число массива я перевожу в строку и прохожу вложенным циклом по этим строкам, добавляя каждый символ в массив `answer` отдельно (с переводом в тип Int).

```
class Solution2553 {
  fun separateDigits(nums: IntArray): IntArray {
        val answer = mutableListOf<Int>()
        for (i in nums) {
            var iString = i.toString()
            for (j in iString)
                answer.add(j.digitToInt())
        }
        return answer.toIntArray()
    }
}
```

### [Задача 1674 (Daily Question from May, 13th](https://leetcode.com/problems/minimum-moves-to-make-array-complementary/description/?envType=daily-question&envId=2026-05-13)
В этой задаче я смотрю на все возможные суммы от 2 до 2 * limit. Именно эти, потому что числа в массиве > 1 и не больше limit. Дальше идея такая: каждой паре может потребоваться 0, 1 или 2 изменения для того чтобы получить нужную сумму. 0 - если они уже составляют нужную сумму, 1 - если при изменении одного из чисел от 1 до limit можно добиться данной суммы [min + 1, max + limit] и 2, если нужно менять оба. 
Чтобы не проходить по каждой возможной сумме для каждой пары отдельно, я использую массив разностей. Смысл в том, что мы не заполняем все значения сразу, а ставим отметки: с какой суммы начинается изменение количества ходов и на какой сумме оно заканчивается. Потом, когда мы проходим по этому массиву слева направо, эти отметки превращаются в значения количества изменений.
Для каждой пары я сначала считаю, что для всех возможных сумм нужно 2 изменения. Затем на диапазоне [min + 1, max + limit] уменьшаю это количество на 1, потому что там достаточно изменить только одно число. После этого в точке a + b уменьшаю ещё на 1, потому что для текущей суммы пары не нужно делать вообще никаких изменений. После обработки всех пар я прохожу по массиву разностей и складываю значения. И потом выбираю сумму, для которой нужно меньше всего изменений.

```
class Solution1674 {
    fun minMoves(nums: IntArray, limit: Int): Int {
        val n = nums.size
        val changes = IntArray(limit * 2 + 2)
        for (i in 0 until n / 2) {
            val a = nums[i]
            val b = nums[n - 1 - i]

            val minVal = minOf(a,b)
            val maxVal = maxOf(a,b)
            val currentSum = a + b
            changes[2] += 2
            changes[2*limit + 1] -= 2

            changes[minVal + 1] -= 1
            changes[maxVal + limit + 1] += 1

            changes[currentSum] -= 1
            changes[currentSum + 1] += 1
        }

        var answer = Int.MAX_VALUE
        var moves = 0
        for (sum in 2..2*limit) {
            moves += changes[sum]
            answer = minOf(answer, moves)
        }

        return answer
    }
}
```
