package com.example.altusmobileapp

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())

            v.setPadding(
                systemBars.left,
                systemBars.top,
                systemBars.right,
                systemBars.bottom
            )

            insets
        }

        configurarBotoesMomentaneos()
    }

    private fun configurarBotoesMomentaneos() {
        // ===================== KIT 1 =====================

        configurarBotaoComLed(
            idBotao = R.id.kit1Btn1,
            idLed = R.id.kit1Led1
        )

        configurarBotaoComLed(
            idBotao = R.id.kit1Btn2,
            idLed = R.id.kit1Led2
        )

        configurarBotaoComLed(
            idBotao = R.id.kit1Btn3,
            idLed = R.id.kit1Led3
        )

        configurarBotaoComLed(
            idBotao = R.id.kit1Btn4,
            idLed = R.id.kit1Led4
        )

        // ===================== KIT 2 =====================

        configurarBotaoComLed(
            idBotao = R.id.kit2Btn1,
            idLed = R.id.kit2Led1
        )

        configurarBotaoComLed(
            idBotao = R.id.kit2Btn2,
            idLed = R.id.kit2Led2
        )

        configurarBotaoComLed(
            idBotao = R.id.kit2Btn3,
            idLed = R.id.kit2Led3
        )

        configurarBotaoComLed(
            idBotao = R.id.kit2Btn4,
            idLed = R.id.kit2Led4
        )
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun configurarBotaoComLed(idBotao: Int, idLed: Int) {
        val botao = findViewById<Button>(idBotao)
        val led = findViewById<View>(idLed)

        // Garante que o LED comece desligado
        led.setBackgroundResource(R.drawable.led_off)

        /*
         * Necessário para acessibilidade.
         * O comportamento principal de segurar/soltar está no setOnTouchListener.
         */
        botao.setOnClickListener {
            // Clique simples não precisa fazer nada neste momento.
        }

        botao.setOnTouchListener { view, event ->
            when (event.action) {

                MotionEvent.ACTION_DOWN -> {
                    // Quando pressiona e segura o botão, liga o LED correspondente
                    led.setBackgroundResource(R.drawable.led_on)
                    true
                }

                MotionEvent.ACTION_UP -> {
                    // Quando solta o botão, desliga o LED correspondente
                    led.setBackgroundResource(R.drawable.led_off)

                    // Chamada recomendada para acessibilidade
                    view.performClick()

                    true
                }

                MotionEvent.ACTION_CANCEL -> {
                    // Caso o toque seja cancelado, garante que o LED apague
                    led.setBackgroundResource(R.drawable.led_off)
                    true
                }

                else -> false
            }
        }
    }
}