package com.example.altusmobileapp.ui

import android.os.Bundle
import android.widget.Button
import android.widget.ScrollView
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.altusmobileapp.R
import java.io.BufferedReader
import java.io.InputStreamReader

class LogViewerActivity : AppCompatActivity() {

    private lateinit var textLogContent: TextView
    private lateinit var logScrollView: ScrollView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_log_viewer)

        val root = findViewById<android.view.View>(R.id.log_viewer_root)
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val basePadding = (16 * resources.displayMetrics.density).toInt()
            
            v.setPadding(
                systemBars.left + basePadding,
                systemBars.top + basePadding,
                systemBars.right + basePadding,
                systemBars.bottom + basePadding
            )
            insets
        }

        textLogContent = findViewById(R.id.textLogContent)
        logScrollView = findViewById(R.id.logScrollView)

        findViewById<Button>(R.id.btnRefreshLogs).setOnClickListener {
            refreshLogs()
        }

        findViewById<Button>(R.id.btnClearLogs).setOnClickListener {
            textLogContent.text = ""
        }

        refreshLogs()
    }

    private fun refreshLogs() {
        try {
            val process = Runtime.getRuntime().exec("logcat -d")
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            val log = StringBuilder()
            var line: String?

            while (bufferedReader.readLine().also { line = it } != null) {
                log.append(line).append("\n")
            }
            
            textLogContent.text = log.toString()

            logScrollView.post {
                logScrollView.fullScroll(ScrollView.FOCUS_DOWN)
            }
            
        } catch (e: Exception) {
            textLogContent.text = "Error to load logs: ${e.message}"
        }
    }
}