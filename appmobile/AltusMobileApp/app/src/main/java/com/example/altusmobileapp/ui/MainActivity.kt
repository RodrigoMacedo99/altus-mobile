package com.example.altusmobileapp.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.MotionEvent
import android.view.View
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.SwitchCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.altusmobileapp.R
import com.example.altusmobileapp.mqtt.MqttConstants

class MainActivity : AppCompatActivity() {

    private val viewModel: MainViewModel by viewModels()

    private val topicToLedMap = mapOf(
        "altus/kit1/pushbutton/1" to R.id.kit1Led1,
        "altus/kit1/pushbutton/2" to R.id.kit1Led2,
        "altus/kit1/pushbutton/3" to R.id.kit1Led3,
        "altus/kit1/pushbutton/4" to R.id.kit1Led4,
        "altus/kit1/switch/1" to R.id.kit1Led5,
        "altus/kit1/switch/2" to R.id.kit1Led6,
        "altus/kit1/switch/3" to R.id.kit1Led7,
        "altus/kit1/switch/4" to R.id.kit1Led8,

        "altus/kit2/pushbutton/1" to R.id.kit2Led1,
        "altus/kit2/pushbutton/2" to R.id.kit2Led2,
        "altus/kit2/pushbutton/3" to R.id.kit2Led3,
        "altus/kit2/pushbutton/4" to R.id.kit2Led4,
        "altus/kit2/switch/1" to R.id.kit2Led5,
        "altus/kit2/switch/2" to R.id.kit2Led6,
        "altus/kit2/switch/3" to R.id.kit2Led7,
        "altus/kit2/switch/4" to R.id.kit2Led8,
    )

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

        setupUI()
        checkMqtt()
    }

    private fun setupUI() {
        val kit1Buttons = listOf(R.id.kit1Btn1, R.id.kit1Btn2, R.id.kit1Btn3, R.id.kit1Btn4)
        val kit1Switches = listOf(R.id.kit1Switch1, R.id.kit1Switch2, R.id.kit1Switch3, R.id.kit1Switch4)

        val kit2Buttons = listOf(R.id.kit2Btn1, R.id.kit2Btn2, R.id.kit2Btn3, R.id.kit2Btn4)
        val kit2Switches = listOf(R.id.kit2Switch1, R.id.kit2Switch2, R.id.kit2Switch3, R.id.kit2Switch4)

        //KIT 1
        kit1Buttons.forEachIndexed { index, viewId ->
            setupPushButton(viewId, kit = 1, id = index + 1)
        }
        kit1Switches.forEachIndexed { index, viewId ->
            setupSwitch(viewId, kit = 1, id = index + 1)
        }

        //KIT 2
        kit2Buttons.forEachIndexed { index, viewId ->
            setupPushButton(viewId, kit = 2, id = index + 1)
        }
        kit2Switches.forEachIndexed { index, viewId ->
            setupSwitch(viewId, kit = 2, id = index + 1)
        }
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun setupPushButton(viewId: Int, kit: Int, id: Int) {
        findViewById<Button>(viewId)?.setOnTouchListener { v, event ->
            when(event.action) {
                MotionEvent.ACTION_DOWN -> {
                    viewModel.sendPushButtonCommand(kit, id, true)
                    true
                }
                MotionEvent.ACTION_UP -> {
                    viewModel.sendPushButtonCommand(kit, id, false)
                    v.performClick()
                    true
                }
                MotionEvent.ACTION_CANCEL -> {
                    viewModel.sendPushButtonCommand(kit, id, false)
                    true
                }
                else -> false
            }
        }
    }

    private fun setupSwitch(viewId: Int, kit: Int, id: Int) {
        findViewById<SwitchCompat>(viewId)?.setOnCheckedChangeListener { _, isChecked ->
            viewModel.sendSwitchCommand(kit, id, isChecked)
        }
    }

    private fun checkMqtt() {
        viewModel.onStatusUpdateReceived = { topic, status ->
            val ledId = topicToLedMap[topic]
            ledId?.let { id ->
                val isTargetOn = status == MqttConstants.PAYLOAD_ON
                val color = if (isTargetOn) R.drawable.led_on else R.drawable.led_off

                findViewById<View>(id)?.setBackgroundResource(color)
            }
        }
    }
}