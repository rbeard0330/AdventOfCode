import scala.collection.mutable.HashSet
import scala.io.Source.fromFile

object Day1 {
  def main(args: Array[String]) =
    val test1 = List(1, 1, 1)
    assert(part_1(test1) == 3)
    println(part_1(changes.toSeq))
    val test2 = List(3, 3, 4, -2, -4)
    assert(part_2(test2) == 10)
    val test3 = List(-6, 3, 8, 5, -6)
    assert(part_2(test3) == 5)
    println(part_2(changes.toSeq))

  def changes =
    for line <- fromFile("inputs/d1.txt").getLines()
      yield line match
        case s"+$pos" => pos.toInt
        case neg => neg.toInt

  def part_1(values: Seq[Int]) =
    values.sum

  def part_2(values: Seq[Int]): Int =
    val repeated = LazyList.continually(values).flatten
    val seen: HashSet[Int] = HashSet()
    var current = 0
    for change <- repeated do
      current += change
      if seen.contains(current) then return current
      seen += current
    0

}
