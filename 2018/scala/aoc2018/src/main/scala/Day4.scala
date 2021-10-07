import scala.io.Source.fromFile

case class Timestamp(year: Int, month: Int, day: Int, hour: Int, minute: Int) extends Ordered[Timestamp]:
  override def compare(that: Timestamp): Int =
    val accessors: Seq[Timestamp => Int] = List(_.year, _.month, _.day, _.hour, _.minute)
    accessors
      .map(accessor => accessor(this) compare accessor(that))
      .filter(_ != 0)
      .headOption
      .getOrElse(0)



object Timestamp:
  def apply(s: String) = s match
    case s"$year-$month-$day $hour:$minute" => new Timestamp(year.toInt, month.toInt, day.toInt, hour.toInt, minute.toInt)

case class Guard(id: Int)
object Guard:
  def apply(s: String) = s match
    case s"Guard #$id" => new Guard(id.toInt)

enum Event:
  case ShiftStart, FallsAsleep, Wakes

case class LogRecord(time: Timestamp, guard: Option[Guard], event: Event) extends Ordered[LogRecord]:
  override def compare(that: LogRecord): Int = this.time compare that.time

object LogRecord:
  def apply(s: String) = s match
    case s"[$time] $guard begins shift" => new LogRecord(Timestamp(time), Some(Guard(guard)), Event.ShiftStart)
    case s"[$time] falls asleep" => new LogRecord(Timestamp(time), None, Event.FallsAsleep)
    case s"[$time] wakes up" => new LogRecord(Timestamp(time), None, Event.Wakes)


case class Shift(guard: Guard, sleepStart: Int, sleepEnd: Int)

object Shift:
  def apply(logs: Seq[LogRecord]) = logs match
    case start +: sleep +: wake +: Nil => new Shift(start.guard.orNull, sleep.time.minute, wake.time.minute)

object Day4 {
  def main(args: Array[String]) =
    assert(Timestamp("1518-11-01 00:00") == Timestamp(1518, 11, 1, 0, 0))
    println(log.take(6))
    println(shifts.take(2))
    println(part_1)

  def part_1 =
    val result = guardSleepMinutes.maxBy[Int]{
      case (guard, (sleeping: Int, mostSlept: Int)) => sleeping
    }
    println(result)
    result match
      case (g: Guard, (sleeping: Int, mostSlept: Int)) => mostSlept * g.id

  def log = fromFile("inputs/d4.txt").getLines().map(LogRecord.apply).toSeq.sorted

  def shifts = log.sliding(3, 3).map(Shift.apply).toSeq

  def guards = shifts.map(_.guard).toSet

  def guardSleepMinutes: Map[Guard, Tuple] = guards
    .map { guard =>
      val guardShifts = shifts
        .filter(_.guard == guard)
      val totalSleeping = guardShifts.map(shift => shift.sleepEnd - shift.sleepStart - 1).sum
      val mostSleptMinute = (0 to 59)
        .map(minute => guardShifts.filter(shift => shift.sleepStart <= minute && shift.sleepEnd > minute).length)
        .zipWithIndex
        .max(Ordering.by(_._2))._1
      guard -> (totalSleeping -> mostSleptMinute)
    }
    .toMap

}
