using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Timers;
using Microsoft.Maui.Dispatching;

namespace Game
{
    /// @class WuerfelViewModel
    /// @brief View model for the dice rolling functionality
    /// @details This class implements the MVVM pattern for handling dice rolling operations
    ///          including animation and result display
    public partial class WuerfelViewModel : ObservableObject
    {
        /// @brief Current dice image path
        /// @details Observable property that holds the current dice face image path
        [ObservableProperty]
        private string diceImage = "dice1.png";

        /// @brief Flag indicating if the result should be shown
        /// @details Observable property that controls the visibility of the dice roll result
        [ObservableProperty]
        private bool showResult;

        /// @brief Text displaying the dice roll result
        /// @details Observable property that holds the text result of the dice roll
        [ObservableProperty]
        private string resultText = "";

        /// @brief Command for rolling the dice
        /// @details IRelayCommand implementation for handling the dice roll action
        public IRelayCommand RollDiceCommand => new RelayCommand(() =>
        {
            var rnd = new Random();
            int value = rnd.Next(1, 7);
            DiceImage = $"dice{value}.png";
            ResultText = $"Ergebnis: {value}";
            ShowResult = true;
        });
    }

}