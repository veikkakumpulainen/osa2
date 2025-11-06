import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # injektoidaan stub Reader
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_existing_player(self):
        player = self.stats.search("Gretzky")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")

    def test_search_returns_none_if_not_found(self):
        player = self.stats.search("Nonexistent")
        self.assertIsNone(player)

    def test_team_returns_all_players_of_given_team(self):
        edm_players = self.stats.team("EDM")
        names = [p.name for p in edm_players]
        self.assertEqual(sorted(names), sorted(["Semenko", "Kurri", "Gretzky"]))

    def test_team_returns_empty_list_if_no_players_in_team(self):
        bos_players = self.stats.team("BOS")
        self.assertEqual(bos_players, [])

    def test_top_returns_correct_number_of_players(self):
        top3 = self.stats.top(2)  # pitäisi palauttaa 3 pelaajaa (0,1,2)
        self.assertEqual(len(top3), 3)

    def test_top_returns_players_in_correct_order(self):
        top1 = self.stats.top(0)  # vain paras
        self.assertEqual(top1[0].name, "Gretzky")  # eniten pisteitä (35+89=124)

    def test_top_includes_tied_scores(self):
        # varmista, ettei järjestys riko jos pisteet samat
        players = self.stats.top(4)
        points = [p.points for p in players]
        self.assertTrue(all(points[i] >= points[i+1] for i in range(len(points)-1)))

if __name__ == "__main__":
    unittest.main()