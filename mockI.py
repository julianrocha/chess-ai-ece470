import chess
import chess.svg
import chess.engine
import time
import math
import random


piece_values = {chess.KING : 20000, chess.QUEEN: 900, chess.ROOK: 500, chess.BISHOP: 330, chess.KNIGHT: 320, chess.PAWN: 100}
# https://www.chessprogramming.org/Simplified_Evaluation_Function

def evaluate_material(board, colour):
	material = 0
	for piece_type in range(chess.PAWN, chess.KING + 1):
		material += piece_values[piece_type] * (len(board.pieces(piece_type, colour)) - len(board.pieces(piece_type, not colour)))
	return material

def evaluate_board(board, colour):
	material = evaluate_material(board, colour)
	# add other evaluations here, examples:
	# deduct for having blocked, doubled, or isolated pawns
	# compare 'mobility' of both sides_
	# add for bishop pair
	# opening book
	# modofied endgame evaluations
	return material

# http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
def find_best_move_AB(board, colour, depth, alpha = -math.inf, beta = math.inf, max_player = True):
	# base case
	if(depth == 0):
		return [evaluate_board(board, colour), None]

	best_move = None
	moves = list(board.legal_moves)
	random.shuffle(moves) # so engine doesn't play the same moves
	# gives_check(move: Move) Probes if the given move would put the opponent in check. The move must be at least pseudo-legal.
	moves.sort(key=lambda move: board.is_capture(move), reverse=True) # pruning is more effective if capture moves are looked at first


	if len(moves) > 0:
		best_move = moves[0] # board.push(None) causes error

	# maximizing player seeks high value boards and vise versa
	best_move_value = -math.inf if max_player else math.inf

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

def play_chess():
	board = chess.Board()
	stockfish = chess.engine.SimpleEngine.popen_uci("/Users/julianrocha/code/stockfish-11-mac/src/stockfish")
	stockfish.configure({"Skill Level" : 1})

	print("Starting chess game...",end="\n")
	while not board.is_game_over():
		print(board)
		if board.turn:
			print("Best move for white is: ",end="")
		else:
			print("Best move for black is: ",end="")
		value, move = find_best_move_AB(board, board.turn, 4)
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
	print("Result for White-Black is: " + board.result())
	if board.is_checkmate():
		print("checkmate!")
	if board.is_stalemate():
		print("stalemate!")
	if board.is_insufficient_material():
		print("insufficient material!")
	if board.has_insufficient_material(chess.WHITE):
		print("white has insufficient material!")
	if board.has_insufficient_material(chess.BLACK):
		print("black has insufficient material!")
	if board.is_seventyfive_moves():
		print("75 moves played without capture/pawn move")
	if board.is_fivefold_repetition():
		print("position occured for 5th time")
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
