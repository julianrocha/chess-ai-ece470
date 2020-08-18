import chess

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

# Corresponds to values for white pieces, mirror square vertically for black value
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