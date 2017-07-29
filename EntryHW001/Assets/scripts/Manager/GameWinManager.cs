using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameWinManager : MonoBehaviour {
    public Button replayButton;
    public Button trapone;
    public Button traptwo;

    public Text winText;

    private void Awake()
    {
        replayButton.gameObject.SetActive(false);
        winText.gameObject.SetActive(false);
    }

    public void GameWin()
    {
        winText.gameObject.SetActive(true);
        replayButton.gameObject.SetActive(true);
        trapone.gameObject.SetActive(false);
        traptwo.gameObject.SetActive(false);
    }
}
