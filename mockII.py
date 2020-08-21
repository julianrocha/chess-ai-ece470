import chess
import chess.svg
import chess.engine
import time
import math
import random

"""
template_square_table = {
	chess.A8: 0, chess.B8: 0, chess.C8: 0, chess.D8: 0, chess.E8: 0, chess.F8: 0, chess.G8: 0, chess.H8: 0,
	chess.A7: 0, chess.B7: 0, chess.C7: 0, chess.D7: 0, chess.E7: 0, chess.F7: 0, chess.G7: 0, chess.H7: 0,
	chess.A6: 0, chess.B6: 0, chess.C6: 0, chess.D6: 0, chess.E6: 0, chess.F6: 0, chess.G6: 0, chess.H6: 0,
	chess.A5: 0, chess.B5: 0, chess.C5: 0, chess.D5: 0, chess.E5: 0, chess.F5: 0, chess.G5: 0, chess.H5: 0,
	chess.A4: 0, chess.B4: 0, chess.C4: 0, chess.D4: 0, chess.E4: 0, chess.F4: 0, chess.G4: 0, chess.H4: 0,
	chess.A3: 0, chess.B3: 0, chess.C3: 0, chess.D3: 0, chess.E3: 0, chess.F3: 0, chess.G3: 0, chess.H3: 0,
	chess.A2: 0, chess.B2: 0, chess.C2: 0, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: 0, chess.H2: 0,
	chess.A1: 0, chess.B1: 0, chess.C1: 0, chess.D1: 0, chess.E1: 0, chess.F1: 0, chess.G1: 0, chess.H1: 0
}
"""

# corresponds to values for white pieces, mirror square vertically for black value
# https://www.chessprogramming.org/Simplified_Evaluation_Function
piece_square_table = {
	chess.PAWN: {
		chess.A8: 0, chess.B8: 0, chess.C8: 0, chess.D8: 0, chess.E8: 0, chess.F8: 0, chess.G8: 0, chess.H8: 0,
		chess.A7: 50, chess.B7: 50, chess.C7: 50, chess.D7: 50, chess.E7: 50, chess.F7: 50, chess.G7: 50, chess.H7: 50,
		chess.A6: 10, chess.B6: 10, chess.C6: 20, chess.D6: 30, chess.E6: 30, chess.F6: 20, chess.G6: 10, chess.H6: 10,
		chess.A5: 5, chess.B5: 5, chess.C5: 10, chess.D5: 25, chess.E5: 25, chess.F5: 10, chess.G5: 5, chess.H5: 5,
		chess.A4: 0, chess.B4: 0, chess.C4: 0, chess.D4: 20, chess.E4: 20, chess.F4: 0, chess.G4: 0, chess.H4: 0,
		chess.A3: 5, chess.B3: -5, chess.C3: -10, chess.D3: 0, chess.E3: 0, chess.F3: -10, chess.G3: -5, chess.H3: 5,
		chess.A2: 5, chess.B2: 10, chess.C2: 10, chess.D2: -20, chess.E2: -20, chess.F2: 10, chess.G2: 10, chess.H2: 5,
		chess.A1: 0, chess.B1: 0, chess.C1: 0, chess.D1: 0, chess.E1: 0, chess.F1: 0, chess.G1: 0, chess.H1: 0
	},
	chess.KNIGHT: {
		chess.A8: -50, chess.B8: -40, chess.C8: -30, chess.D8: -30, chess.E8: -30, chess.F8: -30, chess.G8: -40, chess.H8: -50,
		chess.A7: -40, chess.B7: -20, chess.C7: 0, chess.D7: 0, chess.E7: 0, chess.F7: 0, chess.G7: -20, chess.H7: -40,
		chess.A6: -30, chess.B6: 0, chess.C6: 10, chess.D6: 15, chess.E6: 15, chess.F6: 10, chess.G6: 0, chess.H6: -30,
		chess.A5: -30, chess.B5: 5, chess.C5: 15, chess.D5: 20, chess.E5: 20, chess.F5: 15, chess.G5: 5, chess.H5: -30,
		chess.A4: -30, chess.B4: 0, chess.C4: 15, chess.D4: 20, chess.E4: 20, chess.F4: 15, chess.G4: 0, chess.H4: -30,
		chess.A3: -30, chess.B3: 5, chess.C3: 10, chess.D3: 15, chess.E3: 15, chess.F3: 10, chess.G3: 5, chess.H3: -30,
		chess.A2: -40, chess.B2: -20, chess.C2: 0, chess.D2: 5, chess.E2: 5, chess.F2: 0, chess.G2: -20, chess.H2: -40,
		chess.A1: -50, chess.B1: -40, chess.C1: -30, chess.D1: -30, chess.E1: -30, chess.F1: -30, chess.G1: -40, chess.H1: -50
	},
	chess.BISHOP: {
		chess.A8: -20, chess.B8: -10, chess.C8: -10, chess.D8: -10, chess.E8: -10, chess.F8: -10, chess.G8: -10, chess.H8: -20,
		chess.A7: -10, chess.B7: 0, chess.C7: 0, chess.D7: 0, chess.E7: 0, chess.F7: 0, chess.G7: 0, chess.H7: -10,
		chess.A6: -10, chess.B6: 0, chess.C6: 5, chess.D6: 10, chess.E6: 10, chess.F6: 5, chess.G6: 0, chess.H6: -10,
		chess.A5: -10, chess.B5: 5, chess.C5: 5, chess.D5: 10, chess.E5: 10, chess.F5: 5, chess.G5: 5, chess.H5: -10,
		chess.A4: -10, chess.B4: 0, chess.C4: 10, chess.D4: 10, chess.E4: 10, chess.F4: 10, chess.G4: 0, chess.H4: -10,
		chess.A3: -10, chess.B3: 10, chess.C3: 10, chess.D3: 10, chess.E3: 10, chess.F3: 10, chess.G3: 10, chess.H3: -10,
		chess.A2: -10, chess.B2: 5, chess.C2: 0, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: 5, chess.H2: -10,
		chess.A1: -20, chess.B1: -10, chess.C1: -10, chess.D1: -10, chess.E1: -10, chess.F1: -10, chess.G1: -10, chess.H1: -20
	},
	chess.ROOK: {
		chess.A8: 0, chess.B8: 0, chess.C8: 0, chess.D8: 0, chess.E8: 0, chess.F8: 0, chess.G8: 0, chess.H8: 0,
		chess.A7: 5, chess.B7: 10, chess.C7: 10, chess.D7: 10, chess.E7: 10, chess.F7: 10, chess.G7: 10, chess.H7: 5,
		chess.A6: -5, chess.B6: 0, chess.C6: 0, chess.D6: 0, chess.E6: 0, chess.F6: 0, chess.G6: 0, chess.H6: -5,
		chess.A5: -5, chess.B5: 0, chess.C5: 0, chess.D5: 0, chess.E5: 0, chess.F5: 0, chess.G5: 0, chess.H5: -5,
		chess.A4: -5, chess.B4: 0, chess.C4: 0, chess.D4: 0, chess.E4: 0, chess.F4: 0, chess.G4: 0, chess.H4: -5,
		chess.A3: -5, chess.B3: 0, chess.C3: 0, chess.D3: 0, chess.E3: 0, chess.F3: 0, chess.G3: 0, chess.H3: -5,
		chess.A2: -5, chess.B2: 0, chess.C2: 0, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: 0, chess.H2: -5,
		chess.A1: 0, chess.B1: 0, chess.C1: 0, chess.D1: 5, chess.E1: 5, chess.F1: 0, chess.G1: 0, chess.H1: 0
	},
	chess.QUEEN: {
		chess.A8: -20, chess.B8: -10, chess.C8: -10, chess.D8: -5, chess.E8: -5, chess.F8: -10, chess.G8: -10, chess.H8: -20,
		chess.A7: -10, chess.B7: 0, chess.C7: 0, chess.D7: 0, chess.E7: 0, chess.F7: 0, chess.G7: 0, chess.H7: -10,
		chess.A6: -10, chess.B6: 0, chess.C6: 5, chess.D6: 5, chess.E6: 5, chess.F6: 5, chess.G6: 0, chess.H6: -10,
		chess.A5: -5, chess.B5: 0, chess.C5: 5, chess.D5: 5, chess.E5: 5, chess.F5: 5, chess.G5: 0, chess.H5: -5,
		chess.A4: 0, chess.B4: 0, chess.C4: 5, chess.D4: 5, chess.E4: 5, chess.F4: 5, chess.G4: 0, chess.H4: -5,
		chess.A3: -10, chess.B3: 5, chess.C3: 5, chess.D3: 5, chess.E3: 5, chess.F3: 5, chess.G3: 0, chess.H3: -10,
		chess.A2: -10, chess.B2: 0, chess.C2: 5, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: 0, chess.H2: -10,
		chess.A1: -20, chess.B1: -10, chess.C1: -10, chess.D1: -5, chess.E1: -5, chess.F1: -10, chess.G1: -10, chess.H1: -20
	},
	chess.KING: {
		False: { # piece-square table for middle game
			chess.A8: -30, chess.B8: -40, chess.C8: -40, chess.D8: -50, chess.E8: -50, chess.F8: -40, chess.G8: -40, chess.H8: -30,
			chess.A7: -30, chess.B7: -40, chess.C7: -40, chess.D7: -50, chess.E7: -50, chess.F7: -40, chess.G7: -40, chess.H7: -30,
			chess.A6: -30, chess.B6: -40, chess.C6: -40, chess.D6: -50, chess.E6: -50, chess.F6: -40, chess.G6: -40, chess.H6: -30,
			chess.A5: -30, chess.B5: -40, chess.C5: -40, chess.D5: -50, chess.E5: -50, chess.F5: -40, chess.G5: -40, chess.H5: -30,
			chess.A4: -20, chess.B4: -30, chess.C4: -30, chess.D4: -40, chess.E4: -40, chess.F4: -30, chess.G4: -30, chess.H4: -20,
			chess.A3: -10, chess.B3: -20, chess.C3: -20, chess.D3: -20, chess.E3: -20, chess.F3: -20, chess.G3: -20, chess.H3: -10,
			chess.A2: 20, chess.B2: 20, chess.C2: 0, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: 20, chess.H2: 20,
			chess.A1: 20, chess.B1: 30, chess.C1: 10, chess.D1: 0, chess.E1: 0, chess.F1: 10, chess.G1: 30, chess.H1: 20
		},
		True: { # piece-square table for end game
			chess.A8: -50, chess.B8: -40, chess.C8: -30, chess.D8: -20, chess.E8: -20, chess.F8: -30, chess.G8: -40, chess.H8: -50,
			chess.A7: -30, chess.B7: -20, chess.C7: -10, chess.D7: 0, chess.E7: 0, chess.F7: -10, chess.G7: -20, chess.H7: -30,
			chess.A6: -30, chess.B6: -10, chess.C6: 20, chess.D6: 30, chess.E6: 30, chess.F6: 20, chess.G6: -10, chess.H6: -30,
			chess.A5: -30, chess.B5: -10, chess.C5: 30, chess.D5: 40, chess.E5: 40, chess.F5: 30, chess.G5: -10, chess.H5: -30,
			chess.A4: -30, chess.B4: -10, chess.C4: 30, chess.D4: 40, chess.E4: 40, chess.F4: 30, chess.G4: -10, chess.H4: -30,
			chess.A3: -30, chess.B3: -10, chess.C3: 20, chess.D3: 30, chess.E3: 30, chess.F3: 20, chess.G3: -10, chess.H3: -30,
			chess.A2: -30, chess.B2: -30, chess.C2: 0, chess.D2: 0, chess.E2: 0, chess.F2: 0, chess.G2: -30, chess.H2: -30,
			chess.A1: -50, chess.B1: -30, chess.C1: -30, chess.D1: -30, chess.E1: -30, chess.F1: -30, chess.G1: -30, chess.H1: -50
		}
	}
}

piece_values = {chess.KING : 20000, chess.QUEEN: 900, chess.ROOK: 500, chess.BISHOP: 330, chess.KNIGHT: 320, chess.PAWN: 100}
# https://www.chessprogramming.org/Simplified_Evaluation_Function


# https://www.chessprogramming.org/Simplified_Evaluation_Function
def is_endgame(board):
	if bool(board.pieces(chess.QUEEN, chess.WHITE)):
		if len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.WHITE)) > 1:
			return False # white has queen and more than 1 minor piece
	elif bool(board.pieces(chess.QUEEN, chess.BLACK)):
		if len(board.pieces(chess.KNIGHT, chess.BLACK)) + len(board.pieces(chess.BISHOP, chess.BLACK)) + len(board.pieces(chess.ROOK, chess.BLACK)) > 1:
			return False # black has queen and more than 1 minor piece
	return True # no queens on board, or queens on board but 1 minor piece each maxium

def evaluate_material(board, colour):
	material = 0
	for piece_type in range(chess.PAWN, chess.KING + 1):
		material += piece_values[piece_type] * (len(board.pieces(piece_type, colour)) - len(board.pieces(piece_type, not colour)))
	return material

def evaluate_piece_positions(board, colour):
	score = 0
	for piece_type in range(chess.PAWN, chess.QUEEN + 1):
		for square in board.pieces(piece_type, colour):
			score += piece_square_table[piece_type][square] if colour == chess.WHITE else piece_square_table[piece_type][chess.square_mirror(square)]
		for square in board.pieces(piece_type, not colour):
			score -= piece_square_table[piece_type][square] if colour == chess.BLACK else piece_square_table[piece_type][chess.square_mirror(square)]
	
	endgame = is_endgame(board)
	for square in board.pieces(chess.KING, colour):
		score += piece_square_table[chess.KING][endgame][square] if colour == chess.WHITE else piece_square_table[chess.KING][endgame][chess.square_mirror(square)]
	for square in board.pieces(chess.KING, not colour):
		score -= piece_square_table[chess.KING][endgame][square] if colour == chess.BLACK else piece_square_table[chess.KING][endgame][chess.square_mirror(square)]
	return score

def evaluate_checkmate(board, colour):
	if board.is_checkmate():
		return -math.inf if board.turn == colour else math.inf
	return 0

def evaluate_stalemate(board, material):
	if board.is_stalemate():
		return math.inf if material < 0 else -math.inf
	return 0

def evaluate_board(board, colour):
	material = evaluate_material(board, colour)
	piece_positions = evaluate_piece_positions(board, colour)
	checkmate = evaluate_checkmate(board, colour)
	stalemate = evaluate_stalemate(board, material)

	# rooks on open files (no pawn), semi open (1 pawn)
	# connected rooks
	# pinning pieces, skewer

	# add other evaluations here, examples:
	# deduct for having blocked, doubled, or isolated pawns
	# compare 'mobility' of both sides_
	# add for bishop pair
	# opening book
	# modified endgame evaluations
	return 10 * material + piece_positions + checkmate + stalemate

# http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
def find_best_move_AB(board, colour, depth, alpha = -math.inf, beta = math.inf, max_player = True):
	# base case
	if(depth == 0):
		return [evaluate_board(board, colour), None]

	moves = list(board.legal_moves)
	if len(moves) == 0:
		return [evaluate_board(board, colour), None] # stop descending tree if branch has no legal moves
	
	random.shuffle(moves) # so engine doesn't play the same moves
	moves.sort(key=lambda move: board.is_capture(move), reverse=True) # pruning is more effective if capture moves are looked at first
	best_move = moves[0] # board.push(None) causes error
	best_move_value = -math.inf if max_player else math.inf # maximizing player seeks high value boards and vise versa

	for move in moves:
		board.push(move)

		move_value = find_best_move_AB(board, colour, depth-1, alpha, beta, not max_player)[0]

		if max_player:
			if move_value > best_move_value:
				best_move = move
				best_move_value = move_value 
			alpha = max(move_value, alpha)
		else:
			if move_value < best_move_value:
				best_move = move
				best_move_value = move_value
			beta = min(move_value, beta)

		board.pop()

		if beta <= alpha:
			break

	return [best_move_value, best_move]

def play(board):
	value, move = find_best_move_AB(board, board.turn, 5)
	return [value, move]

def play_chess():
	board = chess.Board()
	stockfish = chess.engine.SimpleEngine.popen_uci("/Users/julianrocha/code/stockfish-11-mac/src/stockfish")
	# stockfish = chess.engine.SimpleEngine.popen_uci("C:/Users/Ryan Russell/Programming/stockfish-11-win/Windows/stockfish_20011801_x64")

	stockfish.configure({"Skill Level" : 5})

	print("Starting chess game...",end="\n")
	while not board.is_game_over():
		
		print(board)
		if board.turn:
			print("Best move for white is: ",end="")
		else:
			print("Best move for black is: ",end="")
		value, move = play(board)
		print(move)
		print(value)
		print()

		board.push(move)

		# stockfish turn as black
		print(board)
		result = stockfish.play(board, chess.engine.Limit(time=0.1))
		if result.move is None:
			break
		print("Stockfish will reply with: " + str(result.move))
		print()
		board.push(result.move)

	stockfish.quit()
	
	if board.is_checkmate():
		print("Checkmate!")
	if board.is_stalemate():
		print("Stalemate!")
	if board.is_insufficient_material():
		print("Insufficient material!")
	if board.has_insufficient_material(chess.WHITE):
		print("White has insufficient material!")
	if board.has_insufficient_material(chess.BLACK):
		print("Black has insufficient material!")
	if board.is_seventyfive_moves():
		print("75 moves played without capture/pawn move")
	if board.is_fivefold_repetition():
		print("Position occurred for 5th time")

	print("Result for White-Black is: " + board.result())

	if board.result() == "0-1":
		print("Stockfish wins.")
	elif board.result() == "1-0":
		print("AI wins.")
	elif board.result() == "1/2-1/2":
		print("The match results in a draw.")
	else:
		print("Result is undetermined.")

	print()
	print(board)

play_chess()

"""
# outdated (no alpha beta pruning), keeping to show the speedup when a/b is used
def find_best_move_NOAB(board, colour, depth, max_player = True):
	# base case
	if(depth == 0):
		return [evaluate_board(board, colour), None]

	best_move = None # TODO: if legal moves is empty then board.push(None) causes error
	moves = list(board.legal_moves)
	random.shuffle(moves) # so engine doesn't play the same moves

	# maximizing player seeks high value boards and vise versa
	best_move_value = -math.inf if max_player else math.inf

	for move in moves:
		board.push(move)

		move_value = find_best_move_NOAB(board, colour, depth-1, not max_player)[0]

		if max_player:
			if move_value > best_move_value:
				best_move = move
				best_move_value = move_value
		else:
			if move_value < best_move_value:
				best_move = move
				best_move_value = move_value

		board.pop()

	return [best_move_value, best_move]
"""
