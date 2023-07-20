#include <GDIPlus.au3>
#include <Array.au3>
#include <Math.au3>
#include <Heap.au3>

Global Const $start[2] = [16, 13]
Global Const $end[2] = [130, 220]

; Load the image and convert it to grayscale
Global $origin_image = _GDIPlus_ImageLoadFromFile('noria.bmp')
Global $img = _GDIPlus_BitmapCreateFromImage($origin_image)
Global $width = _GDIPlus_ImageGetWidth($img)
Global $height = _GDIPlus_ImageGetHeight($img)

; Convert the image to grayscale
_GDIPlus_BitmapConvertFormat($img, $GDIP_PXF_GRAYSCALE)


; Get the image data and convert it to a 2D array
Global $pBits = _GDIPlus_BitmapLockBits($img, 0, 0, $width, $height, $GDIP_ILMREAD, $GDIP_PXF8GRAY)
Global $stride = _GDIPlus_BitmapGetStride($img)
Global $img_arr[$height][$width]
For $y = 0 To $height - 1
	For $x = 0 To $width - 1
	$img_arr[$y][$x] = DllStructGetData(DllStructCreate('byte', $pBits + $y * $stride + $x), 1)
	Next
Next
_GDIPlus_BitmapUnlockBits($img, $pBits)


; Create a new image to draw the path on
Global $path_img = _GDIPlus_BitmapClone($origin_image)
Global $path_graphics = _GDIPlus_ImageGetGraphicsContext($path_img)
_GDIPlus_GraphicsClear($path_graphics, 0xFFFFFFFF)

; Define a function to calculate the Euclidean distance between two points
Func distance($a, $b)
	Local $x1 = $a[0], $y1 = $a[1], $x2 = $b[0], $y2 = $b[1]
	Return Sqrt(($x2 - $x1) ^ 2 + ($y2 - $y1) ^ 2)
EndFunc

; Define a function to check if a point is valid (in bounds and not black)
Func valid_point($p)
	Local $x_ = $p[0], $y_ = $p[1]
	If (0 <= $x_ And $x_ < $width) And (0 <= $y_ And $y_ < $height) Then
		If $img_arr[$y_][$x_] = 0 Then Return False
		Return True
	EndIf
	Return False
EndFunc



; Define the algorithm to find the shortest path between two points
Func find_shortest_path($start, $end)
    Local $pq[0][2] ; priority queue to keep the open set of nodes to visit
    _HeapCreate($pq, 0, 1) ; create the priority queue
    _HeapPush($pq, [0, $start]) ; add the starting node with priority 0

    Local $came_from[$start][2], $cost_so_far[$start] ; to keep track of the parent node and the cost of each path to a visited node
    $came_from[$start] = [0, 0] ; the starting node has no parent
    $cost_so_far[$start] = 0 ; the cost to reach the starting node is 0

    While UBound($pq) > 0 ; while there are still unexplored nodes
        ; get the node with the lowest cost so far from the priority queue
        Local $current_node = _HeapPop($pq)[1], $current_cost = $pq[1][0]

        If $current_node[0] = $end[0] And $current_node[1] = $end[1] Then ; if the end node has been reached, break out of the loop
            ExitLoop
        EndIf

        ; Check the neighbours of the current node
        For $dx = -1 To 1
            For $dy = -1 To 1
                If $dx = 0 And $dy = 0 Then ; skip the current node
                    ContinueLoop 2
                EndIf

                ; Calculate the new position and cost to move to the neighbour node
                Local $neighbour[2] = [$current_node[0] + $dx, $current_node[1] + $dy], $new_cost = $cost_so_far[$current_node] + _distance($current_node, $neighbour)

                ; Check if the neighbour is a valid point and update the path to it
                If _valid_point($neighbour) And (Not IsArray($cost_so_far[$neighbour]) Or $new_cost < $cost_so_far[$neighbour][0]) Then
                    $cost_so_far[$neighbour] = [$new_cost]
                    Local $priority = $new_cost + _distance($end, $neighbour) ; add the Euclidean distance to the end point as priority
                    _HeapPush($pq, [$priority, $neighbour]) ; add the neighbour node with its priority to the priority queue
                    $came_from[$neighbour] = $current_node ; set the parent node for the neighbour node
                EndIf
            Next
        Next
    WEnd

    ; Reconstruct the path by starting from the end node and following the parent nodes back
    Local $path[1][2] = [$end]
    While Not _ArrayCompare($path[$#path], $start) ; while the last element of the path is not the start node
        _ArrayAdd($path, $came_from[$path[$#path]])
    WEnd

    Return _ArrayReverse($path) ; reverse the order of the path to go from start to end
EndFunc



; Use the algorithm to find the shortest path between the start and end points
Global $path = find_shortest_path($start, $end)

; Draw the path on the new image
Local $brush = _GDIPlus_BrushCreateSolid("0xFF00FF00") ; green color
Local $hPen = _GDIPlus_PenCreate($brush, 1) ; width 1
For $i = 0 To UBound($path) - 2
_GDIPlus_GraphicsDrawLine($path_graphics, $path[$i][0], $path[$i][1], $path[$i+1][0], $path[$i+1][1], $hPen)
Next

; Save the path image
_GDIPlus_ImageSaveToFile($path_img, "path.png")