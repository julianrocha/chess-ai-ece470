# Packages
import chess
import chess.svg
import chess.engine
import time
import math
import random
import re

# Files
import values

# https://www.chessprogramming.org/Simplified_Evaluation_Function


def is_endgame(board):
	if bool(board.pieces(chess.QUEEN, chess.WHITE)):
		if len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.WHITE)) > 1:
			return False # white has queen and more than 1 minor piece
	elif bool(board.pieces(chess.QUEEN, chess.BLACK)):
		if len(board.pieces(chess.KNIGHT, chess.BLACK)) + len(board.pieces(chess.BISHOP, chess.BLACK)) + len(board.pieces(chess.ROOK, chess.BLACK)) > 1:
			return False # black has queen and more than 1 minor piece
	return True # no queens on board, or queens on board but 1 minor piece each maxium


def evaluate_piece_positions(board, colour):

	score = 0
	for piece_type in range(chess.PAWN, chess.QUEEN + 1):
		for square in board.pieces(piece_type, colour):
			score += values.piece_square_table[piece_type][square] if colour == chess.WHITE else values.piece_square_table[piece_type][chess.square_mirror(square)]
		for square in board.pieces(piece_type, not colour):
			score -= values.piece_square_table[piece_type][square] if colour == chess.BLACK else values.piece_square_table[piece_type][chess.square_mirror(square)]
	
	endgame = is_endgame(board)
	for square in board.pieces(chess.KING, colour):
		score += values.piece_square_table[chess.KING][endgame][square] if colour == chess.WHITE else values.piece_square_table[chess.KING][endgame][chess.square_mirror(square)]
	for square in board.pieces(chess.KING, not colour):
		score -= values.piece_square_table[chess.KING][endgame][square] if colour == chess.BLACK else values.piece_square_table[chess.KING][endgame][chess.square_mirror(square)]
	return score


def evaluate_material(board, colour):

	material = 0
	for piece_type in range(chess.PAWN, chess.KING + 1):
		material += values.piece_values[piece_type] * (len(board.pieces(piece_type, colour)) - len(board.pieces(piece_type, not colour)))
	return material


def evaluate_board(board, colour):

	material = evaluate_material(board, colour)
	piece_positions = evaluate_piece_positions(board, colour)
	# add other evaluations here, examples:
	# deduct for having blocked, doubled, or isolated pawns
	# compare 'mobility' of both sides_
	# add for bishop pair
	# opening book
	# modified endgame evaluations
	return material + piece_positions


# http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
def find_best_move_AB(board, colour, depth, alpha = -math.inf, beta = math.inf, max_player = True):

	# Base case
	if depth == 0:
		return [evaluate_board(board, colour), None]

	best_move = None
	moves = list(board.legal_moves)
	random.shuffle(moves) # So engine doesn't play the same moves

	# Gives_check(move: Move) Probes if the given move would put the opponent in check. The move must be at least pseudo-legal.
	moves.sort(key=lambda move: board.is_capture(move), reverse=True) # Pruning is more effective if capture moves are looked at first

	if len(moves) > 0:
		best_move = moves[0] # board.push(None) causes error

	# Maximizing player seeks high value boards and vice versa
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


def play_chess(stockfish, colour = '1', manual_play = False):

	board = chess.Board()

	print("Starting chess game...",end="\n")
	while not board.is_game_over():

		print(board)

		if manual_play and colour == '1':
			result = handle_manual_input(board)
			if result is None:
				break
			board.push(result)
		
		if board.turn:
			print("Best move for white is: ",end="")
		else:
			print("Best move for black is: ",end="")
		value, move = find_best_move_AB(board, board.turn, 4)
		print(move)
		print(value)
		print()

		board.push(move)
		print(board)
		print()

		if manual_play == False:
			# Stockfish's turn as black

			result = stockfish.play(board, chess.engine.Limit(time=0.1))

			if result.move is None:
				break
			print("Stockfish will reply with: " + str(result.move))
			print()
			print(result.move)
			board.push(result.move)
		elif colour != '1':

			result = handle_manual_input(board)

			if result is None:
				break

			board.push(result)

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
	return board.result()


def handle_manual_input(board):

	legal_moves = []
	for move in list(board.legal_moves):
		legal_moves.append(str(move))

	print("Legal Moves: ", sorted(legal_moves))
	selected_move = input("Enter move: ")
	
	while selected_move not in legal_moves:
		selected_move = input("Move not legal, please enter a new move: ")
	
	result = chess.Move.from_uci(selected_move)

	print()
	return result


def main():

	usr_choice = input("Enter 1 to play manually, 0 for stockfish: ")

	if usr_choice != '0' and usr_choice != '1':
		print('Please enter a valid input')
		main()
	elif usr_choice == '1':
		colour = input("1 for white, 0 for black: ")
		play_chess(None, colour, True)
	else:
		#stockfish = chess.engine.SimpleEngine.popen_uci("/Users/julianrocha/code/stockfish-11-mac/src/stockfish")
		#stockfish = chess.engine.SimpleEngine.popen_uci("C:/Users/Ryan Russell/Programming/stockfish-11-win/Windows/stockfish_20011801_x64")
		stockfish = chess.engine.SimpleEngine.popen_uci(r"C:\Users\conor\Documents\Summer 2020\ECE 470\stockfish-11-win\Windows\stockfish_20011801_x64_modern.exe")

		stockfish.configure({"Threads" : 8, "Skill Level" : 1})

		results = []
		for i in range(0, 1):
			results.append(play_chess(stockfish))
		print(results)

		stockfish.quit()

main()


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
