using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameOverManager : MonoBehaviour {
    public PlayerHealth playerHealth;
    public float restartDelay = 5f;

    Animator anim;
    float restartTimer;

    public Button replayButton;
    public Button traponeButton;
    public Button traptwoButton;

    private void Awake()
    {
        anim = GetComponent<Animator>();
        replayButton.gameObject.SetActive(false);        
    }

    private void Update()
    {
        if (playerHealth == null)
            return;

        if (playerHealth.currentHealth <= 0)
        {
            anim.SetTrigger("GameOver");
            restartTimer += Time.deltaTime;            
            if (restartTimer >= restartDelay)
            {
                SceneManager.LoadScene("mainscene");
            }
        }
    }

    public void GameOver()
    {
        anim.SetTrigger("GameOver");
        replayButton.gameObject.SetActive(true);

        traponeButton.gameObject.SetActive(false);
        traptwoButton.gameObject.SetActive(false);
    }

    public void ReplayGame()
    {
        GameObject obj = GameObject.FindGameObjectWithTag("NetworkManager");
        GameSceneManager gsm = obj.GetComponent<GameSceneManager>();
        gsm.ReplayGame();
        SceneManager.LoadScene("mainscene");
    }
}
