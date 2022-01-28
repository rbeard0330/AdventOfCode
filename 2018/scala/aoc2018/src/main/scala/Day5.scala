import scala.io.Source.fromFile

type Source = Int;

enum PointStatus:
  case Shared, UnvisitedBorder
  case BorderClaim(owner: Source, claimedAt: Int)
  case Claimed(owner: Source, claimedAt: Int)


object Day5 {
  def main(args: Array[String]) =
    println(findLargest(List(Point(1, 1), Point(1, 6), Point(8, 3), Point(3, 4), Point(5,5), Point(8, 9))))

    // too low 6044
    println(findLargest(sources.toSeq))


  def findLargest(pts: Seq[Point]) =
    var (map, targetSize) = initMap(pts)
    var round = 1
    while map.size < targetSize do
      map = tick(map, round)
      round += 1
    val results = readMap(map)
    println(results)
    // too low 6044
    results.maxBy { item => item._2 }

  def sources =
    for line <- fromFile("aoc2018/inputs/d5.txt").getLines()
      yield line match
        case s"$x, $y" => Point(x.toInt, y.toInt)

  def readMap(map: Map[Point, PointStatus]): Map[Source, Int] =
    var infiniteClaims: Set[Source] = Set()
    var claimSizes: Map[Source, Int] = Map()
    for ((_, status) <- map) do
      status match
        case PointStatus.Claimed(owner, _) => {
          claimSizes = claimSizes.updatedWith(owner)(v => Some(v.getOrElse(0) + 1));
        }
        case PointStatus.BorderClaim(owner, _) => {
          infiniteClaims = infiniteClaims + owner;
        }
        case _ => {}
    claimSizes.filter((item) => !(infiniteClaims contains item._1))


  def initMap(pts: Seq[Point]): (Map[Point, PointStatus], Int) =
    val bounds = Bounds(pts)
    var map: Map[Point, PointStatus] = Map()

    for x <- bounds.x_min to bounds.x_max do
      map = map.updated(Point(x, bounds.y_min), PointStatus.UnvisitedBorder).updated(Point(x, bounds.y_max), PointStatus.UnvisitedBorder)

    for y <- bounds.y_min to bounds.y_max do
      map = map.updated(Point(bounds.x_min, y), PointStatus.UnvisitedBorder).updated(Point(bounds.x_max, y), PointStatus.UnvisitedBorder)

    for ((pt, i) <- pts.zipWithIndex) do
      map = map.updated(pt, PointStatus.Claimed(i, 0))

    (map, bounds.size)


  def tick(map: Map[Point, PointStatus], tickNumber: Int): Map[Point, PointStatus] =
    import PointStatus.*
    map
      .filter(item => item match
        case (_, Claimed(_, priorClaim)) if priorClaim == tickNumber - 1 => true
        case _ => false
      )
      .foldLeft(map) { (currentMap: Map[Point, PointStatus], item: (Point, PointStatus)) =>
        item match
          case (pt, Claimed(source, _)) => pt.neighbors.foldLeft(currentMap) {
            (currentMap: Map[Point, PointStatus], neighbor: Point) =>
              currentMap.updatedWith(neighbor) {
                case Some(Shared) => Some(Shared)
                case Some(BorderClaim(otherClaimOwner, priorClaim)) if otherClaimOwner != source && priorClaim == tickNumber => Some(Shared)
                case Some(Claimed(otherClaimOwner, priorClaim)) if otherClaimOwner != source && priorClaim == tickNumber => Some(Shared)
                case Some(UnvisitedBorder) => Some(BorderClaim(owner = source, claimedAt = tickNumber))
                case None => Some(PointStatus.Claimed(owner = source, claimedAt = tickNumber))
                case other => other
              }
          }
      }


}

case class Point(x: Int, y: Int) {
  def neighbors = Seq((1, 0), (0, 1), (-1, 0), (0, -1)).map((dx, dy) => new Point(this.x + dx, this.y + dy))

  def update(neighbors: Seq[Point]): Point = neighbors match
    case n1 :+ n2 :+ n3 :+ n4 => n2
}

case class Bounds(x_min: Int, x_max: Int, y_min: Int, y_max: Int) {
  def size = (x_max - x_min) * (y_max - y_min)
}

object Bounds {
  def apply(pts: Seq[Point]) =
    val x_coords = pts.map(_.x)
    val y_coords = pts.map(_.y)
    new Bounds(x_coords.min - 10, x_coords.max + 10, y_coords.min - 10, y_coords.max + 10)
}

case class TaggedPoint(pt: Point, owner: Int)